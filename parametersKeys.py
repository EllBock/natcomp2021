parameters = [ 'backward',
               'brakingpacefast',
               'brakingpaceslow',
               'carmaxvisib',
               'carmin',
               'clutchslip',
               'clutchspin',
               'consideredstr8',
               'dnsh1rpm',
               'dnsh2rpm',
               'dnsh3rpm',
               'dnsh4rpm',
               'dnsh5rpm',
               'fullstis',
               'fullstmaxsx',
               'ignoreinfleA',
               'obvious',
               'obviousbase',
               'offroad',
               'oksyp',
               'pointingahead',
               's2cen',
               's2sen',
               'safeatanyspeed',
               'seriousABS',
               'skidsev1',
               'slipdec',
               'sortofontrack',
               'spincutclip',
               'spincutint',
               'spincutslp',
               'st',
               'stC',
               'steer2edge',
               'str8thresh',
               'stst',
               'sxappropriatest1',
               'sxappropriatest2',
               'sycon1',
               'sycon2',
               'upsh2rpm',
               'upsh3rpm',
               'upsh4rpm',
               'upsh5rpm',
               'upsh6rpm',
               'wheeldia',
               'wwlim']

defaultSnakeOilParameters = { 'backward':1.6692247869011361,
               'brakingpacefast': 1.0383418702288039,
               'brakingpaceslow': 2.2425656876338924,
               'carmaxvisib': 2.2918586828736709,
               'carmin': 33.868780217679259,
               'clutchslip': 90.341006943295284,
               'clutchspin': 50.291035172311716,
               'consideredstr8':0.010033102875417081,
               'dnsh1rpm': 4013.503613860325,
               'dnsh2rpm':6313.0396063881408,
               'dnsh3rpm':7018.2574263038514,
               'dnsh4rpm': 7430.3104910837837,
               'dnsh5rpm':7483.4710893801393,
               'fullstis':0.81987358172808966,
               'fullstmaxsx':20.070818862674596,
               'ignoreinfleA':10.793558810628733,
               'obvious':1.3424661801203506,
               'obviousbase':95.307151655731118,
               'offroad': 1.0002653228126588,
               'oksyp':  0.065867064919736679,
               'pointingahead':2.196445074922305,
               's2cen':0.51134607943433941,
               's2sen':3.0044320966938169,
               'safeatanyspeed':0.0012800919243947557,
               'seriousABS':27.913519841072034,
               'skidsev1':0.57661669447984198,
               'slipdec':0.018047798233552067,
               'sortofontrack':1.5040683093640903,
               'spincutclip':0.1025421499370399,
               'spincutint':1.7449866514563273,
               'spincutslp': 0.051425894532076979,
               'st':689.95543662576313,
               'stC':329.15365840061344,
               'steer2edge': 0.95021144003154068,
               'str8thresh': 0.14383741216415255,
               'stst': 494.40788172445616,
               'sxappropriatest1': 16.083269822124979,
               'sxappropriatest2': 0.5520202884372154,
               'sycon1': 0.6429244177717478,
               'sycon2': 1.0002391984331429,
               'upsh2rpm': 9528.4660840537708,
               'upsh3rpm': 9519.1838721046497,
               'upsh4rpm': 9526.724084318208,
               'upsh5rpm': 9652.7871700313972,
               'upsh6rpm': 11914.502728729563,
               'wheeldia': 0.85542776687776345,
               'wwlim': 4.4870482599805364
                              }

notOptimzedParameters = {"brake": 0.00011033489913893834, "backontracksx": 70.850623711341527}
#parameters2 = ['backontracksx', 'backward', 'brake', 'brakingpacefast', 'brakingpaceslow', 'carmaxvisib', 'carmin', 'clutchslip', 'clutchspin', 'consideredstr8', 'dnsh1rpm', 'dnsh2rpm', 'dnsh3rpm', 'dnsh4rpm', 'dnsh5rpm', 'fullstis', 'fullstmaxsx', 'ignoreinfleA', 'obvious', 'obviousbase', 'offroad', 'oksyp', 'pointingahead', 's2cen', 's2sen', 'safeatanyspeed', 'seriousABS', 'skidsev1', 'slipdec', 'sortofontrack', 'spincutclip', 'spincutint', 'spincutslp', 'st', 'stC', 'steer2edge', 'str8thresh', 'stst', 'sxappropriatest1', 'sxappropriatest2', 'sycon1', 'sycon2', 'upsh2rpm', 'upsh3rpm', 'upsh4rpm', 'upsh5rpm', 'upsh6rpm', 'wheeldia', 'wwlim']

minimumValue = [
                0, # backward
                0, # brakingpacefast
                0, # brakingpaceslow
                0, # carmaxvisib
                0, # carmin
                1, # clutchslip
                1, # clutchspin
                0, # consideredstr8
                0, # dnsh1rpm
                0, # dnsh2rpm
                0, # dnsh3rpm
                0, # dnsh4rpm
                0, # dnsh5rpm
                0, # fullstis
                0, # fullstmaxsx
                0, # ignoreinfleA
                0, # obvious
                0, # obviousbase
                0, # offroad
                0.1, # oksyp
                0, # pointingahead
                0, # s2cen
                0, # s2sen
                0, # safeatanyspeed
                0, # seriousABS
                0, # skidsev1
                0, # slipdec
                0, # sortofontrack
                0, # spincutclip
                0, # spincutint
                0, # spincutslp
                50, # st
                20, # stC
                0, # steer2edge
                0, # str8thresh
                50, # stst
                0, # sxappropriatest1
                0, # sxappropriatest2
                0, # sycon1
                0, # sycon2
                1000, # upsh2rpm
                1000, # upsh3rpm
                1000, # upsh4rpm
                1000, # upsh5rpm
                1000, # upsh6rpm
                0, # wheeldia
                0, # wwlim
]

maximumValue = [
                10, # backward
                10, # brakingpacefast
                10, # brakingpaceslow
                10, # carmaxvisib
                100, # carmin
                200, # clutchslip
                200, # clutchspin
                1, # consideredstr8
                10000, # dnsh1rpm
                10000, # dnsh2rpm
                10000, # dnsh3rpm
                10000, # dnsh4rpm
                10000, # dnsh5rpm
                1, # fullstis
                100, # fullstmaxsx
                100, # ignoreinfleA
                100, # obvious
                200, # obviousbase
                100, # offroad
                10, # oksyp
                100, # pointingahead
                10, # s2cen
                10, # s2sen
                10, # safeatanyspeed
                100, # seriousABS
                10, # skidsev1
                10, # slipdec
                10, # sortofontrack
                10, # spincutclip
                10, # spincutint
                10, # spincutslp
                5000, # st
                3000, # stC
                10, # steer2edge
                10, # str8thresh
                5000, # stst
                160, # sxappropriatest1
                10, # sxappropriatest2
                10, # sycon1
                10, # sycon2
                20000, # upsh2rpm
                20000, # upsh3rpm
                20000, # upsh4rpm
                20000, # upsh5rpm
                20000, # upsh6rpm
                10, # wheeldia
                100, # wwlim
]
