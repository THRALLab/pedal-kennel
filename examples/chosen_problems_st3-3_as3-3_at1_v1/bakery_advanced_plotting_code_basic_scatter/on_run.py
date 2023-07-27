from pedal import *
from pedal.extensions.plotting import *
from curriculum_sneks import *
from curriculum_sneks.files import *

salary_file = """Chief Executives|200480|213020|179520
General and Operations Managers|2984920|115250|97970
Legislators|44590|57110|37270
Advertising and Promotions Managers|22520|142860|127150
Marketing Managers|278690|153440|135030
Sales Managers|453800|142390|127490
Public Relations Managers|59850|138000|125780
Fundraising Managers|23190|119400|100810
Administrative Services Managers|224620|113030|100170
Facilities Managers|101230|101970|97930
Computer and Information Systems Managers|485190|162930|159010
Financial Managers|681070|153460|131710
Industrial Production Managers|192270|117780|103150
Purchasing Managers|69310|134590|127150
Transportation, Storage, and Distribution Managers|144640|105580|98230
Compensation and Benefits Managers|15330|139470|127530
Human Resources Managers|166530|136590|126230
Training and Development Managers|35830|128800|120130
Farmers, Ranchers, and Other Agricultural Managers|5220|78440|73060
Construction Managers|284750|108210|98890
Education and Childcare Administrators, Preschool and Daycare|56430|53800|47310
Education Administrators, Kindergarten through Secondary|274710|102650|98420
Education Administrators, Postsecondary|155990|111260|96910
Education Administrators, All Other|49970|94730|90560
Architectural and Engineering Managers|187100|158970|152350
Food Service Managers|210680|63970|59440
Gambling Managers|3660|89190|76910
Entertainment and Recreation Managers, Except Gambling|17800|73810|62000
Lodging Managers|35920|67770|59430
Medical and Health Services Managers|436770|119840|101340
Natural Sciences Managers|74760|156110|137900
Postmasters and Mail Superintendents|12750|81820|80250
Property, Real Estate, and Community Association Managers|234680|70030|59230
Social and Community Service Managers|156400|76790|74000
Emergency Management Directors|10320|84800|76730
Funeral Home Managers|12710|82900|74000
Personal Service Managers, All Other|7350|59580|60360
Managers, All Other|497890|129710|124650
Agents and Business Managers of Artists, Performers, and Athletes|12480|116410|78410
Buyers and Purchasing Agents|439020|72540|63470
Claims Adjusters, Examiners, and Investigators|278140|70960|65080
Insurance Appraisers, Auto Damage|11430|68180|62680
Compliance Officers|334340|75810|71650
Cost Estimators|208950|73740|65170
Human Resources Specialists|740830|70720|62290
Farm Labor Contractors|440|54400|47770
Labor Relations Specialists|63810|77070|77010
Logisticians|189320|79230|77030
Project Management Specialists|743860|98420|94500
Management Analysts|768450|100530|93000
Meeting, Convention, and Event Planners|98150|57850|49470
Fundraisers|82080|64870|60660
Compensation, Benefits, and Job Analysis Specialists|87750|73810|64120
Training and Development Specialists|336030|67620|61570
Market Research Analysts and Marketing Specialists|727540|76080|63920
Business Operations Specialists, All Other|1030330|79240|74670
Accountants and Auditors|1318550|83980|77250
Property Appraisers and Assessors|58340|70050|61340
Budget Analysts|47440|84240|79940
Credit Analysts|68770|88030|77440
Financial and Investment Analysts|291880|103020|91580
Personal Financial Advisors|263030|119960|94170
Insurance Underwriters|107690|79940|76390
Financial Risk Specialists|54320|110610|100000
Financial Examiners|60750|96180|81410
Credit Counselors|31230|50430|47580
Loan Officers|340170|80570|63380
Tax Examiners and Collectors, and Revenue Agents|52270|63200|56780
Tax Preparers|83190|51080|46290
Financial Specialists, All Other|123200|80370|73240
Computer Systems Analysts|505150|102210|99270
Information Security Analysts|157220|113270|102600
Computer and Information Research Scientists|30840|142650|131490
Computer Network Support Specialists|176200|71350|62760
Computer User Support Specialists|654310|57650|49770
Computer Network Architects|168830|120650|120520
Database Administrators|85870|96550|96710
Database Architects|50440|121840|123430
Network and Computer Systems Administrators|316760|91250|80600
Computer Programmers|152610|96650|93000
Software Developers|1364180|120990|120730
Software Quality Assurance Analysts and Testers|190120|97710|98220
Web Developers|84820|81320|77030
Web and Digital Interface Designers|82380|95460|79890
Computer Occupations, All Other|370190|98180|95270
Actuaries|23040|125300|105900
Mathematicians|1770|112430|108100
Operations Research Analysts|98700|95830|82360
Statisticians|31370|99450|95570
Data Scientists|105980|108660|100910
Mathematical Science Occupations, All Other|3970|77960|62460
Architects, Except Landscape and Naval|100400|91900|80180
Landscape Architects|17430|74980|67950
Cartographers and Photogrammetrists|12610|73510|68900
Surveyors|46390|68880|61600
Aerospace Engineers|56640|122970|122270
Agricultural Engineers|1120|87350|82640
Bioengineers and Biomedical Engineers|17190|101020|97410
Chemical Engineers|24180|121840|105550
Civil Engineers|304310|95490|88050
Computer Hardware Engineers|73750|136230|128170
Electrical Engineers|186020|107890|100420
Electronics Engineers, Except Computer|107170|115490|104820
Environmental Engineers|42660|100220|96820
Health and Safety Engineers, Except Mining Safety Engineers and Inspectors|22870|99700|99040
Industrial Engineers|293950|95200|95300
Marine Engineers and Naval Architects|7380|97820|93370
Materials Engineers|21530|101950|98300
Mechanical Engineers|278240|97000|95300
Mining and Geological Engineers, Including Mining Safety Engineers|7370|100450|97090
Nuclear Engineers|12670|121760|120380
Petroleum Engineers|22100|145720|130850
Engineers, All Other|151940|107800|100640
Architectural and Civil Drafters|101310|60620|60340
Electrical and Electronics Drafters|20830|67090|61510
Mechanical Drafters|47760|62650|60200
Drafters, All Other|15300|58330|54240
Aerospace Engineering and Operations Technologists and Technicians|10900|73510|73580
Civil Engineering Technologists and Technicians|64170|58000|58320
Electrical and Electronic Engineering Technologists and Technicians|101450|69070|63640
Electro-Mechanical and Mechatronics Technologists and Technicians|11590|63880|60360
Environmental Engineering Technologists and Technicians|14910|56590|48390
Industrial Engineering Technologists and Technicians|62030|61230|60220
Mechanical Engineering Technologists and Technicians|40180|63390|60460
Calibration Technologists and Technicians|8500|62800|60340
Engineering Technologists and Technicians, Except Drafters, All Other|73600|68290|61950
Surveying and Mapping Technicians|56070|49810|46910
Animal Scientists|2790|80390|65090
Food Scientists and Technologists|13510|84150|78340
Soil and Plant Scientists|15610|76290|66750
Biochemists and Biophysicists|35050|113460|102270
Microbiologists|19430|87820|79260
Zoologists and Wildlife Biologists|15930|70300|64650
Biological Scientists, All Other|47050|90010|82530
Conservation Scientists|22550|68230|63750
Foresters|9500|67710|64110
Epidemiologists|8180|86740|78830
Medical Scientists, Except Epidemiologists|108550|104050|95310
Life Scientists, All Other|6820|94430|81500
Astronomers|1930|139410|128160
Physicists|20020|151580|152430
Atmospheric and Space Scientists|8520|96880|94570
Chemists|80600|89130|79430
Materials Scientists|6690|104790|100090
Environmental Scientists and Specialists, Including Health|76890|81240|76530
Geoscientists, Except Hydrologists and Geographers|23620|103550|83680
Hydrologists|6390|94780|84030
Physical Scientists, All Other|19680|113220|104100
Economists|15640|120830|105630
Survey Researchers|8850|64690|59740
Industrial-Organizational Psychologists|610|113320|105310
Clinical and Counseling Psychologists|58100|99640|82510
School Psychologists|57110|82770|78780
Psychologists, All Other|13800|98010|102900
Sociologists|2640|96260|92910
Urban and Regional Planners|38940|81310|78500
Anthropologists and Archeologists|6650|66800|61910
Geographers|1440|86740|85220
Historians|2910|72130|63940
Political Scientists|5650|120430|122510
Social Scientists and Related Workers, All Other|34330|90900|84430
Agricultural Technicians|13560|44850|40430
Food Science Technicians|11530|47870|46590
Biological Technicians|76150|51770|48140
Chemical Technicians|57690|55040|48990
Environmental Science and Protection Technicians, Including Health|34110|50550|47370
Geological Technicians, Except Hydrologic Technicians|9210|59080|48310
Hydrologic Technicians|3550|71760|62280
Nuclear Technicians|5360|95200|99340
Social Science Research Assistants|28690|56430|49720
Forest and Conservation Technicians|30440|43420|39290
Forensic Science Technicians|17020|66850|61930
Life, Physical, and Social Science Technicians, All Other|62230|55420|49030
Occupational Health and Safety Specialists|106340|78740|77560
Occupational Health and Safety Technicians|21750|57560|51120
Educational, Guidance, and Career Counselors and Advisors|296370|63090|60510
Marriage and Family Therapists|54800|59660|49880
Rehabilitation Counselors|90310|44740|38560
Substance Abuse, Behavioral Disorder, and Mental Health Counselors|310880|53490|48520
Counselors, All Other|29480|49730|45160
Child, Family, and School Social Workers|340050|54880|49150
Healthcare Social Workers|173860|62310|60840
Mental Health and Substance Abuse Social Workers|113810|57800|49130
Social Workers, All Other|49730|63010|61190
Health Education Specialists|55830|64930|60600
Probation Officers and Correctional Treatment Specialists|92140|63290|60250
Social and Human Service Assistants|398380|40460|37610
Community Health Workers|61010|47780|46590
Community and Social Service Specialists, All Other|90770|50510|47390
Clergy|50790|57230|49720
Directors, Religious Activities and Education|21000|52880|46980
Religious Workers, All Other|10490|43290|37500
Lawyers|681010|148030|127990
Judicial Law Clerks|14800|62730|50750
Administrative Law Judges, Adjudicators, and Hearing Officers|13840|104160|102550
Arbitrators, Mediators, and Conciliators|7320|62350|49410
Judges, Magistrate Judges, and Magistrates|27790|142520|148030
Paralegals and Legal Assistants|336250|58330|56230
Title Examiners, Abstractors, and Searchers|51040|52390|47310
Legal Support Workers, All Other|46090|73000|59790
Business Teachers, Postsecondary|79640|105720|94360
Computer Science Teachers, Postsecondary|37600|89610|77910
Mathematical Science Teachers, Postsecondary|44140|87980|77580
Architecture Teachers, Postsecondary|5950|98600|95160
Engineering Teachers, Postsecondary|35440|115590|104940
Agricultural Sciences Teachers, Postsecondary|8570|97520|95910
Biological Science Teachers, Postsecondary|47690|98710|81440
Forestry and Conservation Science Teachers, Postsecondary|1180|93510|82330
Atmospheric, Earth, Marine, and Space Sciences Teachers, Postsecondary|10250|102840|98070
Chemistry Teachers, Postsecondary|20260|94060|79410
Environmental Science Teachers, Postsecondary|5440|92210|81980
Physics Teachers, Postsecondary|12460|99480|93070
Anthropology and Archeology Teachers, Postsecondary|5010|102110|97340
Area, Ethnic, and Cultural Studies Teachers, Postsecondary|9040|91680|78910
Economics Teachers, Postsecondary|11790|124090|104940
Geography Teachers, Postsecondary|3440|88150|81440
Political Science Teachers, Postsecondary|14060|98980|81980
Psychology Teachers, Postsecondary|36060|88390|77860
Sociology Teachers, Postsecondary|12550|87850|77980
Social Sciences Teachers, Postsecondary, All Other|16140|87320|77500
Health Specialties Teachers, Postsecondary|191830|133310|102720
Nursing Instructors and Teachers, Postsecondary|68060|82040|77440
Education Teachers, Postsecondary|58780|76990|63910
Library Science Teachers, Postsecondary|4330|80850|77100
Criminal Justice and Law Enforcement Teachers, Postsecondary|13790|81730|64600
Law Teachers, Postsecondary|14110|130820|123470
Social Work Teachers, Postsecondary|12280|77650|71010
Art, Drama, and Music Teachers, Postsecondary|94720|86240|75940
Communications Teachers, Postsecondary|27330|84580|77560
English Language and Literature Teachers, Postsecondary|58480|82680|75930
Foreign Language and Literature Teachers, Postsecondary|19640|82990|77030
History Teachers, Postsecondary|18590|86460|78130
Philosophy and Religion Teachers, Postsecondary|20850|88260|77610
Family and Consumer Sciences Teachers, Postsecondary|2730|93230|79630
Recreation and Fitness Studies Teachers, Postsecondary|13860|79080|72440
Career/Technical Education Teachers, Postsecondary|105440|63130|59840
Postsecondary Teachers, All Other|199020|92200|78160
Preschool Teachers, Except Special Education|391670|36460|30210
Kindergarten Teachers, Except Special Education|120730|64490|60900
Elementary School Teachers, Except Special Education|1329280|67080|61400
Middle School Teachers, Except Special and Career/Technical Education|592000|66880|61320
Career/Technical Education Teachers, Middle School|11840|69410|61820
Secondary School Teachers, Except Special and Career/Technical Education|1020240|69530|61820
Career/Technical Education Teachers, Secondary School|84360|68960|61820
Special Education Teachers, Preschool|21130|71970|62420
Special Education Teachers, Kindergarten and Elementary School|187070|67090|61640
Special Education Teachers, Middle School|79070|68860|61820
Special Education Teachers, Secondary School|145690|70100|62120
Special Education Teachers, All Other|38000|71330|61720
Adult Basic Education, Adult Secondary Education, and English as a Second Language Instructors|38260|60650|59720
Self-Enrichment Teachers|216910|49230|43580
Substitute Teachers, Short-Term|374620|38410|30100
Tutors|147100|41780|36470
Teachers and Instructors, All Other|164650|62200|50540
Archivists|6120|61880|60050
Curators|11030|63880|60110
Museum Technicians and Conservators|10960|52030|47630
Librarians and Media Collections Specialists|127790|64180|61190
Library Technicians|73000|39070|36970
Farm and Home Management Educators|10620|58040|49990
Instructional Coordinators|184740|70560|63740
Teaching Assistants, Postsecondary|121290|41170|38040
Teaching Assistants, Except Postsecondary|1187270|31760|29360
Educational Instruction and Library Workers, All Other|155950|49650|46300
Art Directors|42080|115430|100890
Craft Artists|3740|40730|35930
Fine Artists, Including Painters, Sculptors, and Illustrators|9430|69010|60820
Special Effects Artists and Animators|20430|86220|78790
Artists and Related Workers, All Other|7390|67240|61580
Commercial and Industrial Designers|27940|79680|77030
Fashion Designers|19310|83650|77450
Floral Designers|36000|32100|29880
Graphic Designers|204040|59970|50710
Interior Designers|61970|62570|60340
Merchandise Displayers and Window Trimmers|159790|35520|32060
Set and Exhibit Designers|6850|62960|54860
Designers, All Other|10190|73480|62310
Producers and Directors|138250|101950|79000
Athletes and Sports Competitors|12320|116930|77300
Coaches and Scouts|193740|50550|38970
Umpires, Referees, and Other Sports Officials|9620|51710|35860
Choreographers|3990|49630|42700
Music Directors and Composers|9560|65080|49130
Broadcast Announcers and Radio Disc Jockeys|24580|56110|37630
News Analysts, Reporters, and Journalists|39080|63230|48370
Public Relations Specialists|242710|73250|62800
Editors|88780|76400|63350
Technical Writers|47620|81470|78060
Writers and Authors|49410|81120|69510
Interpreters and Translators|52170|58400|49110
Court Reporters and Simultaneous Captioners|12300|65240|60380
Media and Communication Workers, All Other|16540|59400|49900
Audio and Video Technicians|50590|55310|48820
Broadcast Technicians|25270|51280|44740
Sound Engineering Technicians|10800|67360|60500
Lighting Technicians|4280|58020|51470
Photographers|38420|48210|38950
Camera Operators, Television, Video, and Film|20280|61740|49230
Film and Video Editors|28030|76000|62680
Media and Communication Equipment Workers, All Other|16670|69290|63250
Chiropractors|35810|81240|75000
Dentists, General|108680|167160|160370
Prosthodontists|790|143730|100950
Dentists, All Other Specialists|4750|179400|175160
Dietitians and Nutritionists|66690|65620|61650
Optometrists|38720|125440|124300
Pharmacists|312550|125690|128570
Physician Assistants|132940|119460|121530
Podiatrists|8840|158380|145840
Occupational Therapists|127830|89470|85570
Physical Therapists|225350|92920|95620
Radiation Therapists|16050|94000|82790
Recreational Therapists|16980|53900|47940
Respiratory Therapists|133410|68190|61830
Speech-Language Pathologists|147470|85820|79060
Exercise Physiologists|6860|54030|47940
Therapists, All Other|13490|65030|59500
Veterinarians|77260|109920|100370
Registered Nurses|3047530|82750|77600
Nurse Anesthetists|43950|202470|195610
Nurse Midwives|7750|114210|112830
Nurse Practitioners|234690|118040|120680
Audiologists|13240|86050|78950
Pediatricians, General|33620|198420|170480
Acupuncturists|7250|71770|60570
Dental Hygienists|207190|81360|77810
Healthcare Diagnosing or Treating Practitioners, All Other|26250|113230|100300
Clinical Laboratory Technologists and Technicians|318780|56910|57800
Cardiovascular Technologists and Technicians|55760|62020|60570
Diagnostic Medical Sonographers|78640|80680|77740
Nuclear Medicine Technologists|17140|84850|78760
Radiologic Technologists and Technicians|216380|66490|61370
Magnetic Resonance Imaging Technologists|38070|77820|77360
Medical Dosimetrists|2400|124750|127270
Emergency Medical Technicians|161400|36690|35470
Paramedics|96510|49500|46770
Dietetic Technicians|21610|34160|29520
Pharmacy Technicians|436630|37970|36740
Psychiatric Technicians|93410|38000|36570
Surgical Technologists|109060|53590|48530
Veterinary Technologists and Technicians|118670|38250|36850
Ophthalmic Medical Technicians|65700|41120|37180
Licensed Practical and Licensed Vocational Nurses|641240|51850|48070
Medical Records Specialists|180570|48310|46660
Opticians, Dispensing|73270|43060|37570
Orthotists and Prosthetists|10410|79820|75440
Hearing Aid Specialists|10790|59960|59500
Health Technologists and Technicians, All Other|140770|49230|45720
Health Information Technologists and Medical Registrars|37900|61410|55560
Athletic Trainers|26070|54650|48420
Genetic Counselors|2740|86640|80150
Surgical Assistants|17250|59170|48320
Healthcare Practitioners and Technical Workers, All Other|44100|64880|58750
Home Health and Personal Care Aides|3366480|29260|29430
Nursing Assistants|1314830|33250|30310
Orderlies|45160|33440|29990
Psychiatric Aides|39140|34640|30260
Occupational Therapy Assistants|41980|63560|61730
Occupational Therapy Aides|3370|39230|33560
Physical Therapist Assistants|93660|60740|61180
Physical Therapist Aides|42390|30370|29200
Massage Therapists|81030|49260|46910
Dental Assistants|347170|42510|38660
Medical Assistants|727760|38190|37190
Medical Equipment Preparers|61170|42420|38220
Medical Transcriptionists|55830|34220|30100
Pharmacy Aides|43560|34560|29930
Veterinary Assistants and Laboratory Animal Caretakers|98970|31780|29780
Phlebotomists|132750|38450|37380
Healthcare Support Workers, All Other|108410|40690|37740
First-Line Supervisors of Correctional Officers|54470|69750|62220
First-Line Supervisors of Police and Detectives|128230|98760|99330
First-Line Supervisors of Firefighting and Prevention Workers|80890|83270|78230
First-Line Supervisors of Security Workers|55450|55080|50240
First-Line Supervisors of Protective Service Workers, All Other|23780|63910|61010
Firefighters|317310|55290|50700
Fire Inspectors and Investigators|14600|69680|64600
Forest Fire Inspectors and Prevention Specialists|2770|54340|42600
Bailiffs|16420|52340|48320
Correctional Officers and Jailers|392600|53420|47920
Detectives and Criminal Investigators|107890|90370|83640
Fish and Game Wardens|6730|58190|60730
Parking Enforcement Workers|7450|46050|46590
Police and Sheriff's Patrol Officers|665380|70750|64610
Transit and Railroad Police|3590|69570|64930
Animal Control Workers|11600|42620|39160
Private Detectives and Investigators|28860|60970|59380
Gambling Surveillance Officers and Gambling Investigators|9190|38080|35450
Security Guards|1057100|35830|31470
Crossing Guards and Flaggers|82690|35670|31450
Lifeguards, Ski Patrol, and Other Recreational Protective Service Workers|114320|27320|25630
Transportation Security Screeners|48320|46380|45470
School Bus Monitors|55310|30220|29100
Protective Service Workers, All Other|100110|42160|38210
Chefs and Head Cooks|129810|56920|50160
First-Line Supervisors of Food Preparation and Serving Workers|1040600|39150|36570
Cooks, Fast Food|768130|25490|24180
Cooks, Institution and Cafeteria|392860|31520|29910
Cooks, Private Household|440|43260|42920
Cooks, Restaurant|1193860|31630|30010
Cooks, Short Order|124800|28110|28560
Cooks, All Other|18170|33390|30720
Food Preparation Workers|783350|28810|28780
Bartenders|485330|30340|26350
Fast Food and Counter Workers|3095120|26060|25100
Waiters and Waitresses|1804030|29010|26000
Food Servers, Nonrestaurant|243030|29500|28730
Dining Room and Cafeteria Attendants and Bartender Helpers|336970|27690|27170
Dishwashers|377040|27350|28130
Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop|324690|26000|24600
Food Preparation and Serving Related Workers, All Other|83240|28760|29120
First-Line Supervisors of Housekeeping and Janitorial Workers|153640|45100|39630
First-Line Supervisors of Landscaping, Lawn Service, and Groundskeeping Workers|116380|53270|48800
Janitors and Cleaners, Except Maids and Housekeeping Cleaners|2036680|31860|29760
Maids and Housekeeping Cleaners|723430|29580|28780
Building Cleaning Workers, All Other|17350|38530|34350
Pest Control Workers|85370|40640|37540
Landscaping and Groundskeeping Workers|892450|35240|34430
Pesticide Handlers, Sprayers, and Applicators, Vegetation|25820|40500|38270
Tree Trimmers and Pruners|41920|47450|46970
Grounds Maintenance Workers, All Other|15770|39120|36540
First-Line Supervisors of Gambling Services Workers|19510|52590|49140
First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services|66860|47130|44870
First-Line Supervisors of Personal Service Workers|101030|45730|40390
Animal Trainers|15840|38230|31280
Animal Caretakers|225680|29520|28600
Gambling Dealers|64700|28960|24960
Gambling and Sports Book Writers and Runners|7340|29110|27530
Gambling Service Workers, All Other|10820|31790|28990
Motion Picture Projectionists|1620|32970|29350
Ushers, Lobby Attendants, and Ticket Takers|54970|26390|24440
Amusement and Recreation Attendants|262170|26110|24500
Costume Attendants|3380|54590|47850
Locker Room, Coatroom, and Dressing Room Attendants|9670|30220|28570
Entertainment Attendants and Related Workers, All Other|4290|29680|24170
Embalmers|4070|51210|47780
Crematory Operators|2040|39660|37490
Funeral Attendants|32490|31630|29230
Morticians, Undertakers, and Funeral Arrangers|24700|56360|48950
Barbers|12910|35700|29970
Hairdressers, Hairstylists, and Cosmetologists|285980|35990|29670
Makeup Artists, Theatrical and Performance|1960|124380|134750
Manicurists and Pedicurists|120540|30480|29210
Shampooers|9560|25160|24440
Skincare Specialists|50580|41700|37300
Baggage Porters and Bellhops|20530|30040|29120
Concierges|33560|37520|35210
Tour and Travel Guides|30980|33200|29780
Childcare Workers|438520|27680|27490
Exercise Trainers and Group Fitness Instructors|221600|45870|40700
Recreation Workers|264020|32020|29680
Residential Advisors|92500|34950|31220
Personal Care and Service Workers, All Other|72030|30790|29610
First-Line Supervisors of Retail Sales Workers|1143260|46890|39230
First-Line Supervisors of Non-Retail Sales Workers|243920|92320|79680
Cashiers|3318020|26770|27260
Gambling Change Persons and Booth Cashiers|17150|29130|28600
Counter and Rental Clerks|371620|36170|31330
Parts Salespersons|265130|36920|34260
Retail Salespersons|3693490|31920|29120
Advertising Sales Agents|96660|66540|52340
Insurance Sales Agents|422600|69340|49840
Securities, Commodities, and Financial Services Sales Agents|426870|93260|62910
Travel Agents|37190|46580|43810
Sales Representatives of Services, Except Advertising, Insurance, Financial Services, and Travel|1026390|71110|60550
Sales Representatives, Wholesale and Manufacturing, Technical and Scientific Products|266160|102750|94840
Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products|1242490|72390|61600
Demonstrators and Product Promoters|40680|36990|32350
Real Estate Brokers|48460|86490|62010
Real Estate Sales Agents|175920|61480|48340
Sales Engineers|59550|118630|103710
Telemarketers|115130|30670|28910
Door-to-Door Sales Workers, News and Street Vendors, and Related Workers|7860|34970|29390
Sales and Related Workers, All Other|235740|38840|29570
First-Line Supervisors of Office and Administrative Support Workers|1443630|63380|60590
Switchboard Operators, Including Answering Service|48190|34590|30150
Telephone Operators|3870|39370|37630
Communications Equipment Operators, All Other|1340|49470|47000
Bill and Account Collectors|212900|41280|37700
Billing and Posting Clerks|429080|42750|38330
Bookkeeping, Accounting, and Auditing Clerks|1509370|45140|45560
Gambling Cage Workers|11140|30770|29360
Payroll and Timekeeping Clerks|149290|49560|47610
Procurement Clerks|61930|44930|45150
Tellers|364210|34930|36310
Financial Clerks, All Other|30310|47830|46900
Brokerage Clerks|39980|57710|54000
Correspondence Clerks|7060|41710|37920
Court, Municipal, and License Clerks|150170|44870|44610
Credit Authorizers, Checkers, and Clerks|16820|44540|44710
Customer Service Representatives|2787070|39070|36920
Eligibility Interviewers, Government Programs|151340|48570|47420
File Clerks|85460|36820|36360
Hotel, Motel, and Resort Desk Clerks|220380|28040|28080
Interviewers, Except Eligibility and Loan|169840|38840|37220
Library Assistants, Clerical|78470|32490|29450
Loan Interviewers and Clerks|238610|44910|45940
New Accounts Clerks|40500|41250|37840
Order Clerks|133850|41820|37920
Human Resources Assistants, Except Payroll and Timekeeping|102770|44840|45630
Receptionists and Information Clerks|983150|32910|29950
Reservation and Transportation Ticket Agents and Travel Clerks|100860|45630|39900
Information and Record Clerks, All Other|155080|43950|43160
Cargo and Freight Agents|85750|48420|46910
Couriers and Messengers|68310|34270|33050
Public Safety Telecommunicators|97050|47030|46670
Dispatchers, Except Police, Fire, and Ambulance|194330|46650|44050
Meter Readers, Utilities|24000|47430|45720
Postal Service Clerks|79320|53210|52290
Postal Service Mail Carriers|335540|54370|52440
Postal Service Mail Sorters, Processors, and Processing Machine Operators|112130|51010|48550
Production, Planning, and Expediting Clerks|367200|52220|48040
Shipping, Receiving, and Inventory Clerks|795360|38210|36890
Weighers, Measurers, Checkers, and Samplers, Recordkeeping|54760|39540|37610
Executive Secretaries and Executive Administrative Assistants|466910|66870|62060
Legal Secretaries and Administrative Assistants|155250|52540|47710
Medical Secretaries and Administrative Assistants|656640|39740|37450
Secretaries and Administrative Assistants, Except Legal, Medical, and Executive|1825980|41080|37880
Data Entry Keyers|147170|35940|35630
Word Processors and Typists|41930|43370|44030
Desktop Publishers|7600|50930|46910
Insurance Claims and Policy Processing Clerks|218300|45790|45520
Mail Clerks and Mail Machine Operators, Except Postal Service|69400|34390|32550
Office Clerks, General|2578180|38990|37030
Office Machine Operators, Except Computer|32920|37110|36630
Proofreaders and Copy Markers|5340|46010|43940
Statistical Assistants|6190|53420|48160
Office and Administrative Support Workers, All Other|147140|42580|37900
First-Line Supervisors of Farming, Fishing, and Forestry Workers|25770|54450|48640
Agricultural Inspectors|13630|47430|45140
Animal Breeders|950|43270|40090
Graders and Sorters, Agricultural Products|25560|30400|29630
Agricultural Equipment Operators|26180|36280|36360
Farmworkers and Laborers, Crop, Nursery, and Greenhouse|277200|31440|29630
Farmworkers, Farm, Ranch, and Aquacultural Animals|34140|32150|29630
Agricultural Workers, All Other|6100|37190|32550
Forest and Conservation Workers|6300|33690|30550
Fallers|4170|53760|47700
Logging Equipment Operators|25510|43960|46400
Log Graders and Scalers|3260|41520|37820
Logging Workers, All Other|3080|45430|46090
First-Line Supervisors of Construction Trades and Extraction Workers|665870|75060|72010
Boilermakers|12920|69070|64290
Brickmasons and Blockmasons|55950|61430|59340
Stonemasons|9000|50170|47610
Carpenters|668060|55190|48260
Carpet Installers|19790|48710|46640
Floor Layers, Except Carpet, Wood, and Hard Tiles|18300|53880|48060
Floor Sanders and Finishers|4340|44380|39140
Tile and Stone Setters|41160|53330|47810
Cement Masons and Concrete Finishers|186600|50900|47340
Terrazzo Workers and Finishers|2640|58380|48680
Construction Laborers|968760|44130|37770
Paving, Surfacing, and Tamping Equipment Operators|44200|50590|46960
Pile Driver Operators|3760|75950|76260
Operating Engineers and Other Construction Equipment Operators|404820|56280|48360
Drywall and Ceiling Tile Installers|97070|54810|48040
Tapers|14580|65140|61080
Electricians|650580|63310|60040
Glaziers|52700|51950|47180
Insulation Workers, Floor, Ceiling, and Wall|30360|44810|39880
Insulation Workers, Mechanical|28010|56260|48260
Painters, Construction and Maintenance|214220|47140|45590
Paperhangers|2340|51560|47610
Pipelayers|33330|48510|45980
Plumbers, Pipefitters, and Steamfitters|417620|63350|59880
Plasterers and Stucco Masons|26980|54810|48340
Reinforcing Iron and Rebar Workers|16420|58960|48830
Roofers|129890|48890|47110
Sheet Metal Workers|122630|58760|53440
Structural Iron and Steel Workers|68620|61270|58550
Solar Photovoltaic Installers|16420|50710|47670
Helpers--Brickmasons, Blockmasons, Stonemasons, and Tile and Marble Setters|18210|43370|37870
Helpers--Carpenters|27540|37340|36690
Helpers--Electricians|72150|36720|36360
Helpers--Painters, Paperhangers, Plasterers, and Stucco Masons|8940|35270|33370
Helpers--Pipelayers, Plumbers, Pipefitters, and Steamfitters|45930|36350|35720
Helpers--Roofers|6830|36000|36360
Helpers, Construction Trades, All Other|27300|37610|36690
Construction and Building Inspectors|117830|68480|61640
Elevator and Escalator Installers and Repairers|22510|91320|97860
Fence Erectors|24470|41140|37700
Hazardous Materials Removal Workers|44240|49280|46300
Highway Maintenance Workers|141150|44340|45880
Rail-Track Laying and Maintenance Equipment Operators|21030|60770|61690
Septic Tank Servicers and Sewer Pipe Cleaners|28620|45390|44810
Miscellaneous Construction and Related Workers|30920|45370|39850
Derrick Operators, Oil and Gas|7880|52140|47230
Rotary Drill Operators, Oil and Gas|11170|61840|56380
Service Unit Operators, Oil and Gas|32870|55660|48410
Excavating and Loading Machine and Dragline Operators, Surface Mining|35720|49850|46740
Earth Drillers, Except Oil and Gas|15800|53600|48250
Explosives Workers, Ordnance Handling Experts, and Blasters|5370|57070|53040
Continuous Mining Machine Operators|14740|57430|60300
Roof Bolters, Mining|1850|59170|59770
Loading and Moving Machine Operators, Underground Mining|4450|57330|57900
Underground Mining Machine Operators, All Other|3150|60290|61260
Rock Splitters, Quarry|4450|41630|37700
Roustabouts, Oil and Gas|34520|44730|38920
Helpers--Extraction Workers|5980|40860|37760
Extraction Workers, All Other|5380|50960|48140
First-Line Supervisors of Mechanics, Installers, and Repairers|526240|73590|71260
Computer, Automated Teller, and Office Machine Repairers|86420|44170|40970
Radio, Cellular, and Tower Equipment Installers and Repairers|13700|62500|60360
Telecommunications Equipment Installers and Repairers, Except Line Installers|172830|60350|60370
Avionics Technicians|18910|69860|69280
Electric Motor, Power Tool, and Related Repairers|15880|48740|46910
Electrical and Electronics Installers and Repairers, Transportation Equipment|10710|70650|77250
Electrical and Electronics Repairers, Commercial and Industrial Equipment|50780|64230|61730
Electrical and Electronics Repairers, Powerhouse, Substation, and Relay|22490|87640|93420
Electronic Equipment Installers and Repairers, Motor Vehicles|9000|43690|40670
Audiovisual Equipment Installers and Repairers|21540|46120|44790
Security and Fire Alarm Systems Installers|77420|52170|48320
Aircraft Mechanics and Service Technicians|125440|69470|65380
Automotive Body and Related Repairers|137300|50660|47270
Automotive Glass Installers and Repairers|16230|40690|37920
Automotive Service Technicians and Mechanics|629780|47990|46880
Bus and Truck Mechanics and Diesel Engine Specialists|261420|53020|48690
Farm Equipment Mechanics and Service Technicians|35030|47250|46910
Mobile Heavy Equipment Mechanics, Except Engines|145230|57280|58030
Rail Car Repairers|22800|60400|60250
Motorboat Mechanics and Service Technicians|23080|46660|46730
Motorcycle Mechanics|15020|41970|38170
Outdoor Power Equipment and Other Small Engine Mechanics|34700|40360|37540
Bicycle Repairers|14760|34360|34690
Recreational Vehicle Service Technicians|16030|44930|43560
Tire Repairers and Changers|93180|32520|29580
Mechanical Door Repairers|23300|45520|45060
Control and Valve Installers and Repairers, Except Mechanical Door|44870|67310|62760
Heating, Air Conditioning, and Refrigeration Mechanics and Installers|356960|54690|48630
Home Appliance Repairers|28120|45340|44320
Industrial Machinery Mechanics|373090|58780|59840
Maintenance Workers, Machinery|57660|53570|48900
Millwrights|39240|61260|60330
Refractory Materials Repairers, Except Brickmasons|660|54760|54250
Electrical Power-Line Installers and Repairers|123940|79060|78310
Telecommunications Line Installers and Repairers|101530|62250|60190
Camera and Photographic Equipment Repairers|2340|44260|38200
Medical Equipment Repairers|53400|56420|49910
Musical Instrument Repairers and Tuners|5710|39740|37160
Watch and Clock Repairers|1970|45460|44250
Precision Instrument and Equipment Repairers, All Other|11110|59070|57670
Maintenance and Repair Workers, General|1416740|44920|43180
Wind Turbine Service Technicians|10100|58580|56260
Coin, Vending, and Amusement Machine Servicers and Repairers|27540|42010|39040
Commercial Divers|2670|82010|60360
Locksmiths and Safe Repairers|15380|47810|46910
Manufactured Building and Mobile Home Installers|3530|35830|36360
Riggers|17980|52100|48130
Signal and Track Switch Repairers|8090|74220|80570
Helpers--Installation, Maintenance, and Repair Workers|88480|35090|33100
Installation, Maintenance, and Repair Workers, All Other|164070|45380|42570
First-Line Supervisors of Production and Operating Workers|629420|67330|61790
Aircraft Structure, Surfaces, Rigging, and Systems Assemblers|33320|55380|49480
Coil Winders, Tapers, and Finishers|11090|42460|38360
Electrical, Electronic, and Electromechanical Assemblers, Except Coil Winders, Tapers, and Finishers|271920|39630|37460
Engine and Other Machine Assemblers|45990|48110|47440
Structural Metal Fabricators and Fitters|61070|45730|45480
Fiberglass Laminators and Fabricators|17380|40360|37650
Timing Device Assemblers and Adjusters|560|44670|37780
Miscellaneous Assemblers and Fabricators|1328550|37780|36590
Bakers|181800|32300|29750
Butchers and Meat Cutters|145930|35670|36050
Meat, Poultry, and Fish Cutters and Trimmers|132100|31680|29730
Slaughterers and Meat Packers|86450|32010|29900
Food and Tobacco Roasting, Baking, and Drying Machine Operators and Tenders|21050|36280|35480
Food Batchmakers|155240|36190|35780
Food Cooking Machine Operators and Tenders|26710|35430|35890
Food Processing Workers, All Other|46360|33600|31890
Extruding and Drawing Machine Setters, Operators, and Tenders, Metal and Plastic|59490|40520|37750
Forging Machine Setters, Operators, and Tenders, Metal and Plastic|11500|44410|44520
Rolling Machine Setters, Operators, and Tenders, Metal and Plastic|31650|46210|46210
Cutting, Punching, and Press Machine Setters, Operators, and Tenders, Metal and Plastic|179630|40000|37630
Drilling and Boring Machine Tool Setters, Operators, and Tenders, Metal and Plastic|6810|43240|38580
Grinding, Lapping, Polishing, and Buffing Machine Tool Setters, Operators, and Tenders, Metal and Plastic|67750|40030|37550
Lathe and Turning Machine Tool Setters, Operators, and Tenders, Metal and Plastic|19690|44270|44240
Milling and Planing Machine Setters, Operators, and Tenders, Metal and Plastic|14920|47100|46850
Machinists|333220|49020|47730
Metal-Refining Furnace Operators and Tenders|15540|46440|46690
Pourers and Casters, Metal|6570|44910|45850
Model Makers, Metal and Plastic|3690|59080|55630
Patternmakers, Metal and Plastic|2090|49840|48090
Foundry Mold and Coremakers|13610|39980|37710
Molding, Coremaking, and Casting Machine Setters, Operators, and Tenders, Metal and Plastic|163210|37530|36370
Multiple Machine Tool Setters, Operators, and Tenders, Metal and Plastic|134880|40830|37630
Tool and Die Makers|63630|56150|57000
Welders, Cutters, Solderers, and Brazers|397600|48290|47010
Welding, Soldering, and Brazing Machine Setters, Operators, and Tenders|29980|42950|38580
Heat Treating Equipment Setters, Operators, and Tenders, Metal and Plastic|14540|41560|38450
Layout Workers, Metal and Plastic|6840|52340|51690
Plating Machine Setters, Operators, and Tenders, Metal and Plastic|32310|38580|37200
Tool Grinders, Filers, and Sharpeners|6100|43660|38430
Metal Workers and Plastic Workers, All Other|18740|39480|36990
Prepress Technicians and Workers|25840|43800|42610
Printing Press Operators|145290|41120|37770
Print Binding and Finishing Workers|40810|37060|36590
Laundry and Dry-Cleaning Workers|157400|27830|28350
Pressers, Textile, Garment, and Related Materials|26910|28110|28680
Sewing Machine Operators|116220|30880|29690
Shoe and Leather Workers and Repairers|5620|34890|31450
Shoe Machine Operators and Tenders|3610|29920|28560
Sewers, Hand|4170|31350|29930
Tailors, Dressmakers, and Custom Sewers|17270|35430|31420
Textile Bleaching and Dyeing Machine Operators and Tenders|6240|31940|29930
Textile Cutting Machine Setters, Operators, and Tenders|11970|33100|29960
Textile Knitting and Weaving Machine Setters, Operators, and Tenders|16330|33640|33990
Textile Winding, Twisting, and Drawing Out Machine Setters, Operators, and Tenders|22160|33050|30020
Extruding and Forming Machine Setters, Operators, and Tenders, Synthetic and Glass Fibers|14040|40600|37550
Fabric and Apparel Patternmakers|3220|64070|58650
Upholsterers|28020|38220|37420
Textile, Apparel, and Furnishings Workers, All Other|12750|32840|29750
Cabinetmakers and Bench Carpenters|93070|40070|37540
Furniture Finishers|16300|37310|36580
Model Makers, Wood|340|60040|60780
Patternmakers, Wood|210|51020|46920
Sawing Machine Setters, Operators, and Tenders, Wood|45350|35280|35340
Woodworking Machine Setters, Operators, and Tenders, Except Sawing|67210|35560|36090
Woodworkers, All Other|7910|36080|35610
Nuclear Power Reactor Operators|4820|111220|104260
Power Distributors and Dispatchers|9660|95520|98530
Power Plant Operators|28960|83740|80850
Stationary Engineers and Boiler Operators|29820|70510|63500
Water and Wastewater Treatment Plant and System Operators|121150|52320|47880
Chemical Plant and System Operators|21740|69020|70200
Gas Plant Operators|15110|76970|77850
Petroleum Pump System Operators, Refinery Operators, and Gaugers|34230|80500|79540
Plant and System Operators, All Other|15420|55480|50250
Chemical Equipment Operators and Tenders|106170|52450|48090
Separating, Filtering, Clarifying, Precipitating, and Still Machine Setters, Operators, and Tenders|48620|47060|46030
Crushing, Grinding, and Polishing Machine Setters, Operators, and Tenders|31800|42790|38760
Grinding and Polishing Workers, Hand|15680|35990|35670
Mixing and Blending Machine Setters, Operators, and Tenders|108440|42490|38420
Cutters and Trimmers, Hand|7920|34330|30230
Cutting and Slicing Machine Setters, Operators, and Tenders|55930|40010|37810
Extruding, Forming, Pressing, and Compacting Machine Setters, Operators, and Tenders|56570|40050|37660
Furnace, Kiln, Oven, Drier, and Kettle Operators and Tenders|14180|43910|43710
Inspectors, Testers, Sorters, Samplers, and Weighers|551380|44810|38580
Jewelers and Precious Stone and Metal Workers|24350|47090|46640
Dental Laboratory Technicians|34150|47320|45770
Medical Appliance Technicians|15300|46320|45280
Ophthalmic Laboratory Technicians|18930|38910|37270
Packaging and Filling Machine Operators and Tenders|358640|36750|35960
Painting, Coating, and Decorating Workers|11850|38250|37330
Coating, Painting, and Spraying Machine Setters, Operators, and Tenders|145410|43900|39130
Semiconductor Processing Technicians|24020|45910|39870
Photographic Process Workers and Processing Machine Operators|5740|40300|36590
Computer Numerically Controlled Tool Operators|157840|46240|46640
Computer Numerically Controlled Tool Programmers|25800|62360|60780
Adhesive Bonding Machine Operators and Tenders|12510|38580|37630
Cleaning, Washing, and Metal Pickling Equipment Operators and Tenders|13580|35820|35090
Cooling and Freezing Equipment Operators and Tenders|7500|42910|40390
Etchers and Engravers|7110|36970|36590
Molders, Shapers, and Casters, Except Metal and Plastic|38420|39020|37500
Paper Goods Machine Setters, Operators, and Tenders|87480|44180|44820
Tire Builders|17240|47840|47940
Helpers--Production Workers|202860|32910|30000
Production Workers, All Other|204500|36230|32930
Aircraft Cargo Handling Supervisors|8590|62080|53540
First-Line Supervisors of Transportation and Material Moving Workers, Except Aircraft Cargo Handling Supervisors|549260|58580|54850
Airline Pilots, Copilots, and Flight Engineers|81310|198190|202180
Commercial Pilots|42770|115080|99640
Air Traffic Controllers|21230|127920|129750
Airfield Operations Specialists|12610|54360|47880
Flight Attendants|96900|62280|61640
Ambulance Drivers and Attendants, Except Emergency Medical Technicians|11710|31060|29120
Driver/Sales Workers|477020|31970|29280
Heavy and Tractor-Trailer Truck Drivers|1903420|50340|48310
Light Truck Drivers|1010040|42630|38280
Bus Drivers, School|361420|38750|37910
Bus Drivers, Transit and Intercity|145720|51310|48620
Shuttle Drivers and Chauffeurs|175660|32570|30000
Taxi Drivers|13950|30050|29310
Motor Vehicle Operators, All Other|48690|36410|30600
Locomotive Engineers|38980|72940|79740
Rail Yard Engineers, Dinkey Operators, and Hostlers|4460|58070|61090
Railroad Brake, Signal, and Switch Operators and Locomotive Firers|16200|63050|63840
Railroad Conductors and Yardmasters|48030|66990|63960
Subway and Streetcar Operators|10310|71520|81180
Rail Transportation Workers, All Other|1140|54140|47590
Sailors and Marine Oilers|26610|57800|46720
Captains, Mates, and Pilots of Water Vessels|33490|98330|81640
Motorboat Operators|2740|44410|38670
Ship Engineers|7650|96910|82410
Bridge and Lock Tenders|4040|44760|45390
Parking Attendants|91160|29210|29240
Automotive and Watercraft Service Attendants|111480|29960|29330
Aircraft Service Attendants|12170|38640|36390
Traffic Technicians|7770|53210|48610
Transportation Inspectors|25070|77620|79770
Passenger Attendants|21240|34380|30470
Transportation Workers, All Other|13750|39990|36880
Conveyor Operators and Tenders|28650|37010|36420
Crane and Tower Operators|43400|65270|62240
Dredge Operators|1650|50530|46210
Hoist and Winch Operators|2610|58450|52300
Industrial Truck and Tractor Operators|758290|40950|38380
Cleaners of Vehicles and Equipment|351960|30550|29280
Laborers and Freight, Stock, and Material Movers, Hand|2729010|34950|31230
Machine Feeders and Offbearers|60880|36660|37010
Packers and Packagers, Hand|585270|30950|29940
Stockers and Order Fillers|2451430|33020|30110
Gas Compressor and Gas Pumping Station Operators|2910|67130|70720
Pump Operators, Except Wellhead Pumpers|10600|54400|49580
Wellhead Pumpers|16040|67170|63740
Refuse and Recyclable Material Collectors|126050|42780|38500
Tank Car, Truck, and Ship Loaders|12090|55330|49390
Material Moving Workers, All Other|22470|40190|36150"""

suppress("algorithmic", "iterating_over_non_list")
suppress("algorithmic", "iterating_over_empty_list")
suppress("algorithmic", "incompatible_types")

prevent_advanced_iteration(allow_for=True)

ensure_import('matplotlib.pyplot')
ensure_import('bakery_salary')

ensure_ast("For")
ensure_literal([], message="You will need to create a new empty list to solve this.")
ensure_ast("Attribute", message="You need to use attribute access to get the fields.")
ensure_import('matplotlib.pyplot', message="You have not imported the <code>matplotlib.pyplot</code> module.")

prevent_incorrect_plt()
ensure_correct_plot('scatter')
ensure_show()
ensure_function_call('title', message="You need to add a title.")
ensure_function_call('xlabel', message="You need to label your X-axis.")
ensure_function_call('ylabel', message="You need to label your Y-axis.")

from dataclasses import dataclass

@dataclass
class Industry:
    """
    Information about an individual industry.
    
    Attributes:
        name: The name of the industry
        members: The number of people employed in the industry.
        mean_salary: The average salary of people in this industry.
        median_salary: The median salary of people in this industry (more robust to outliers).
    """
    name: str
    members: int
    mean_salary: int
    median_salary: int

industries = []
for line in salary_file.split('\n'):
    name, members, mean, median = line.split("|")
    industries.append(Industry(
        name, int(members), int(mean), int(median)
    ))


means = [i.mean_salary for i in industries]
medians = [i.median_salary for i in industries]
members = [i.members for i in industries]
assert_plot('scatter', [means, medians])
assert_plot('scatter', [means, members])

plots = get_plots()
if len(plots) < 2:
    gently("You need to create multiple, separate graphs.")
elif len(plots) > 2:
    gently("You have created too many graphs.")
else:
    if not plots[0]['data'] or not plots[1]['data']:
        gently("It seems like one of your plots may be empty. Make sure you have two separate plots, each with its own data.")
