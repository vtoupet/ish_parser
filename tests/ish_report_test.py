import unittest
import datetime
from src.ish_report import ish_report, ish_reportException

class ish_report_test(unittest.TestCase):

  def test_single_reading(self):
    noaa_string = """0243725300948462014010101087+41995-087934FM-16+0205KORD V0302905N00155004575MN0020125N5-01115-01445999999ADDAA101000231AU110030015AW1715GA1085+004575991GD14991+0045759GE19MSL   +99999+99999GF199999990990004571991991MA1102615100145REMMET10912/31/13 19:08:03 SPECI KORD 010108Z 29003KT 1 1/4SM -SN OVC015 M11/M14 A3030 RMK AO2 P0001 T11111144 $ (KLC)"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(2014, 01, 01))
    self.assertEquals(weather.wban, '94846')
    self.assertEquals(weather.weather_station, '725300')
    self.assertEquals(weather.report_type, 'FM-16')
    self.assertEquals(weather.latitude, 41.995)
    self.assertEquals(weather.longitude, -87.934)
    self.assertEquals(weather.visibility_distance, 2012)
    self.assertEquals(weather.air_temperature, -12)
    self.assertEquals(len(weather.precipitation), 1)
    precip = weather.precipitation[0]
    self.assertEquals(precip['hours'], 1)
    self.assertEquals(precip['depth'], 0.2)

  def test_present_weather(self):
    noaa_string = """0281725300948462014010508237+41995-087934FM-16+0205KORD V0303505N00625005795MN0020125N5-00565-00835999999ADDAA101000531AU110030015AW1715GA1025+003355991GA2085+005795991GD11991+0033559GD24991+0057959GE19MSL   +99999+99999GF199999990990003351991991MA1101665099215REMMET11601/05/14 02:23:02 SPECI KORD 050823Z 35012KT 1 1/4SM -SN FEW011 OVC019 M06/M08 A3002 RMK AO2 P0002 T10561083 $ (MJF)"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.present_weather, 
                      [{'descriptor': '', 'intensity': 'Light', 'precipitation': 'Snow'}])
    self.assertEquals(weather.precipitation, [{'depth': 0.5, 'hours': 1}])

  def test_report_with_big_quality_section(self):
    noaa = """0177330580999991970050200004+52050+033950FM-12+999999999V0201401N00621220001CN0190001N9+01501+00611100651ADDAA199000091AY121999GA1021+003009079GA2999+999999099GF199999999999999999001001MD1710041+9999EQDQ01+000002SCOTCVQ02+000002SCOTLCQ03+000002SCOLCGQ04+000992SCOLCBQ05    003SCCGA2"""
    weather = ish_report()
    weather.loads(noaa)
    self.assertEquals(weather.datetime.date(), datetime.date(1970,5,2))

  def test_fm15(self):
    noaa_string = """0250725300948462014010100517+41995-087934FM-15+0205KORD V0302505N00155005795MN0024145N5-01115-01445102735ADDAA101000895AU110030015AW1715GA1085+005795991GD14991+0057959GE19MSL   +99999+99999GF199999990990005791991991MA1102575100115REMMET11612/31/13 18:51:03 METAR KORD 010051Z 25003KT 1 1/2SM -SN OVC019 M11/M14 A3029 RMK AO2 SLP273 P0003 T11111144 $ (KLC)"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(2014, 01, 01))
    self.assertEquals(weather.wban, '94846')
    self.assertEquals(weather.weather_station, '725300')
    self.assertEquals(weather.report_type, 'FM-15')
    self.assertEquals(weather.elevation, 205)
    self.assertEquals(weather.wind_speed, 1.5)
    self.assertEquals(weather.wind_speed.get_miles(), 3.3554)
    self.assertEquals(weather.wind_direction, 250)
    self.assertEquals(weather.sky_ceiling, 579)
    self.assertEquals(weather.air_temperature, -12)
    self.assertEquals(weather.air_temperature.get_fahrenheit(), 10.4)
    self.assertEquals(weather.sea_level_pressure, 1027.3)

  def test_austin(self):
    string = """0190722540139042014042819537+30183-097680FM-15+0151KAUS V0203505N004152200059N0160935N5+03175+00065100325ADDAA101000095GA1005+999999999GD10991+9999999GF100991999999999999999999MA1100445098655REMMET09504/28/14 13:53:02 METAR KAUS 281953Z 35008KT 10SM CLR 32/01 A2966 RMK AO2 SLP032 T03170006 (JP)"""
    weather = ish_report()
    weather.loads(string)
    self.assertRaises(BaseException, weather.get_additional_field, 'AJ1')

  def test_boston(self):
    string = """0253725090147392005010101547+42361-071011FM-15+0009KBOS V0202305N00675018295MN0160935N5+00785+00335102175ADDAA101000025GA1075+018295999GA2085+025915999GD13991+0182959GD24991+0259159GF108991999999999999999999MA1102175102065MW1001REMMET12112/31/04 20:54:26 METAR KBOS 010154Z 23013KT 10SM BKN060 OVC085 08/03 A3017 RMK AO2 RAB23E32 SLP217 P0000 T00780033 (ETM)"""
    weather = ish_report()
    weather.loads(string)
    self.assertEquals(weather.air_temperature.get_fahrenheit(), 44.6)
    self.assertEquals(weather.wind_speed, 6.7)
    self.assertEquals(weather.report_type, 'METAR Aviation routine weather report')
    self.assertEquals(weather.wind_direction, 230)

  def test_snowfall(self):
    string = """0479725300948462014010105517+41995-087934FM-15+0205KORD V0300105N00465007015MN0028165N5-01225-01565102655ADDAA101001095AA206005691AJ100089500007694AU110030015AW1715GA1075+007015991GA2075+011285991GA3085+016765991GD13991+0070159GD23991+0112859GD34991+0167659GE19MSL   +99999+99999GF199999990990007011991991KA1060M-01111KA2060N-01221KA3240M-01111KA4240N-01671MA1102515100045MD1690154+9999REMMET17012/31/13 23:51:03 METAR KORD 010551Z 01009KT 1 3/4SM -SN BKN023 BKN037 OVC055 M12/M16 A3027 RMK AO2 SLP265 4/003 P0005 60022 T11221156 11111 21122 411111167 56015 $ (SMN)EQDQ01  00558PRCP06"""
    weather = ish_report()
    weather.loads(string)
    self.assertEquals(weather.wind_direction, 10)
    self.assertEquals(weather.datetime.date(), datetime.date(2014, 01, 01))
    self.assertEquals(weather.snow_depth, [{'depth': 8, 'quality': '5', 'condition': '9'}])
    self.assertEquals(len(weather.precipitation), 2)

  def test_random_sod_file(self):
    noaa_string = """0141725300948462008020205596+41986-087914SOD  +0205KORD V030999999999999999999999999999+99999+99999999999ADDAA124003691AJ100159199999999AN1024008999KA1025M-00111KA2025N-00441MG1098959999999OE11240116234099999OE22240093906099999OE33240045699999999"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(2008, 02, 02))
    precip = weather.precipitation[0]
    self.assertEquals(precip['hours'], 24)
    self.assertEquals(precip['depth'], 3.6) 

  def test_another_random_string(self):
    noaa_string = """041572530094846198002081200C+41983-087900SAO  +0201ORD  V02099959000050076249N0128005N1-00565-00785103405ADDAA101000095AG12000AJ100089199999999AY121999GA1999+007624064GD14085+9999999GD20995+9999999GD30995+9999999GD40995+9999999GF108085081051008001999999KA1999M-00171KA2999N-00561MA1103321100815MD1510001+9999MW1021WG199190199999EQDQ01    003PRSWM1N01 00000JPWTH 1QNNE11 1 00610E11 1 00099E11 1 00099E11 1 00099G11 1 00025H11 1 15025K11 1 00018L11 1 00800M11 1 29770N11 1 00000Q11 1 10340S11 1 00022V11 1 01010X11 1 00000"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(1980, 02, 8))

  def test_crazy_remarks(self):
    noaa_string = """1434725300948462006030105596+41986-087914SOM  +0205KORD V030999999999999999999999999999+99999+99999999999ADDAB10045799AD10030291516999999999AE1079039019019AK1002531299999AM1003091111999999995AN1672006499KB1672N-06675KB2672M+02395KB3672A-02115KC1N9-02161899995KC2M9+01331499995KD1672H10246KD2672C00005KE1079009289019MH109925U101799MK1104171810215100070305395REMSOM882PCP MTOT:1.80 DEPNRM:+0.2 PCP GT 24HRS:1.19 DATE(S):15-16 DAYS W/PCP >=.01:7  DAYS W/PCP >=.10:3  DAYS W/ PCP >=.50:1 DAYS W/PCP >=1.00:1 MSDP AMTS W/DATE-TIME TAGS:MIN:5 0.00    /     MIN:10 0.00    /     MIN:15 0.00    /     MIN:20 0.00    /     MIN:30 0.00    /     MIN:45 0.00    /     MIN:60 0.00    /     MIN:80 0.00    /     MIN:100 0.00    /     MIN:120 0.00    /     MIN:150 0.00    /     MIN:180 0.00    /     SN GT DP ON GRND:1 DATE(S):12 SN GT IN 24HRS:1.2 DATE(S): 11SN MTOT:2.5 AVG DLY MIN:20.0  AVG DLY MAX:36.3  AVG MLY TMP:28.2  DEP NORM:1.2   MIN TMP:-7 DATE(S):18 MAX TMP:56  DATE(S):14 DAYS MAX <=32:7 DAYS MAX >=90:0  DAYS MIN <=32:28 DAYS MIN  <=0:1  AVG STP:29.305 LWST SLP:29.55 DATE/TIME:030539 HGST SLP:30.76 DATE/TIME:181021 HDD MTH TOT:1024 DEP NORM:-51 SEASON(JUL 1-JUN 30):4259 DEP NORM:-587 CDD MTH TOT:0 DEP NORM: 0 SEASON(JAN 1-DEC 31):0 DEP NORM: 0EQDR01  1.807ABP070R02  1.197ADP081R03     17AE2103R04  0.007A01001R05  0.007A02007R06  0.007A03013R07  0.007A04019R08  0.007A05026R09  0.007A06033R10  0.007A07039R11  0.007A08046R12  0.007A09052R13  0.007A10058R14  0.007A11065R15  0.007A12071R16   2.57ANS075R17  10247KDH045R18     17KE4041"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.datetime.date(), datetime.date(2006, 3, 1))

  def test_with_crazy_metar_in_remarks(self):
    """ this one has some crazy double remarks thing going on """
    noaa_string = """033072530094846197301312200C+41983-087900SAO  +0201ORD  V0201405N00525004574MN0096005N1+00395+00115101305ADDAA101000095GD14995+0045099GD20995+9999999GD30995+9999999GD40995+9999999GF108085999999999999999999MA1101251098815MW1041MW2051MW3445REMAWY012VA?ORD C1/78MET005?1/30EQDN01 07200JPWTH 1QNNE11 1 00699E11 1 00099E11 1 00099E11 1 00099G11 1 00015K11 1 00034L11 1 00600M11 1 29180N11 1 07200Q11 1 10130S11 1 00039V11 1 01010X11 1 14010"""
    weather = ish_report()
    weather.loads(noaa_string)
    self.assertEquals(weather.wind_direction, 140)
    self.assertEquals(weather.datetime.date(), datetime.date(1973, 1, 31))

  def test_Weird_old_report(self):
    noaa = """0078035480999991943070121004+52467+000950FM-12+004699999V0209991N00671999991CN0040001N9+99999+99999999999ADDAY121999GA1081+999999999GF199999071051004501999999MW1051EQDQ01+000072SCOTCV"""
    ish = ish_report()
    ish.loads(noaa)
    self.assertEquals(ish.air_temperature, 999)
    self.assertEquals(ish.wind_speed, 6.7)
    self.assertEquals(str(ish.wind_direction), 'MISSING')
    self.assertEquals(ish.wind_direction, 999)
    self.assertEquals(str(ish.sky_ceiling), 'MISSING')
    self.assertEquals(ish.air_temperature.get_fahrenheit(), 'MISSING')
    self.assertEquals(str(ish.sea_level_pressure), 'MISSING')

  def test_bad_length(self):
    noaa_string = """1243725300948462014010101087+41995-087934FM-16+0205KORD V0302905N00155004575MN0020125N5-01115-01445999999ADDAA101000231AU110030015AW1715GA1085+004575991GD14991+0045759GE19MSL   +99999+99999GF199999990990004571991991MA1102615100145REMMET10912/31/13 19:08:03 SPECI KORD 010108Z 29003KT 1 1/4SM -SN OVC015 M11/M14 A3030 RMK AO2 P0001 T11111144 $ (KLC)"""
    self.assertRaises(ish_reportException, 
                      ish_report().loads, noaa_string)

  def test_old_ord(self):
    ''' test an old ORD record from 1946 that has a bunch of missing fields '''
    noaa = """0066725300948461946100109004+41983-087900SAO  +0186ORD  V02099999999992200019N0032001N9+99999+99999999999ADDGA1001+999999999GF100991999999999999999999MA1999999100341MW1111"""
    ish = ish_report()
    ish.loads(noaa)
    self.assertEquals(ish.datetime, datetime.datetime(1946,10,1,9))
    self.assertEquals(str(ish.air_temperature), 'MISSING')
    self.assertEquals(str(ish.wind_speed), 'MISSING')
    self.assertEquals(ish.sky_ceiling, 22000)
    self.assertEquals(str(ish.sea_level_pressure), 'MISSING')

  def test_string_that_caused_infinite_recursion(self):
    noaa = """0059035480999991943070124004+52467+000950FM-12+004699999V0200501N00461220001CN0040001N9+99999+99999999999ADDAY121999GA1001+999999999GF108991081051004501999999MW1051"""
    ish = ish_report()
    ish.loads(noaa)
    self.assertEquals(ish.datetime, datetime.datetime(1943, 07, 2, 0, 0))
    self.assertEquals(ish.air_temperature.get_fahrenheit(), 'MISSING')
    self.assertEquals(ish.sea_level_pressure, 9999.9)
    self.assertEquals(str(ish.sea_level_pressure), 'MISSING')
    self.assertEquals(str(ish.sky_ceiling), '22000')
