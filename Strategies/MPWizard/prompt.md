MP wizard execution logic 

[ ] Risk 1.25% of total capital per trade
[ ] Set weekday option SL value for each instrument
[ ] Set low medium high IB range for each instrument. 
[ ] IB > 0.25ATR5d = SmallIB
[ ] 0.25ATR5d <IB > 0.75ATR5d= MediumIB
[ ] IB > 0.75ATR5d = BigIB
[ ] Trigger points: 1hr IB H and L
[ ] For SmallIB : ATM CE option at UpCross and ATM PE option at DownCross
[ ] For MediumIB: ATM CE option at upcross and ATM CE option at downcross (PE on both upcross and downcross if "MarketMood": "Bearish")
[ ] For BigIB: ATM PE option at upcross and ATM CE option at downcross.
[ ] Only 1 trade per instrument per day.
[ ] Calculate average % of total capital based on margin utilized each day for each instrument

############################ MPWizard.json ###########################

{
	"indices": [{
			"name": "Nifty", #Fixed
			"token": 256265, #Fixed
			"NextExpiry": "06Jul23", #Updated Weekly
			"InstruMood": "Bullish", #Manual
            "OptionRegime": "Buy", #Manual
			"InTrade": false, # Updated every Minute			
            "WeekdayPrcRef": {
                "Mon": 18,
				"Tue": 21,
				"Wed": 24,
				"Thu": 25,
				"Fri": 15 
            }, #Fixed
            "ATR5D": 120.00, #Updated Daily (9:05 AM)
            "IBValue": 45.00, #Updated Daily (10.15 AM)
            "IBLevel": "Medium", #Updated Daily (10.15 AM)			
			"TriggerPoints": {
				"IBHigh": 19072.50, #Updated Daily (10.15 AM)
				"IBLow": 19015.50	#Updated Daily (10.15 AM)			
			}
            "TSLStepSize": 0.5, #Manual
            "SignalEntry": {
                "Option": NIFTY06Jul2319100CE,
                "Event": "Bullish-MediumIB-IBHighUpcross",
				"EntryTime": 10:45:29AM,
				"EntryPrice": 85.50,
                "ExitTime": 03:12:22PM,
                "ExitPrice": 159.45			
			}, # Updated every minute
		},
		{
			"name": "BankNifty",
			"token": 260105,
			"NextExpiry": "06Jul23",
			"InstruMood": "Bullish",
            "OptionRegime": "Buy", #Manual
			"InTrade": false,
			"CompletedTrades": 0,
            "WeekdayPrcRef": {
                "Mon": 50,
				"Tue": 65,
				"Wed": 80,
				"Thu": 90,
				"Fri": 40
            },
            "ATR5D": 380.00,
            "IBValue": 180.00,
            "IBLevel": "Medium",
			"TriggerPoints": {
				"IBHigh": 40200.50,
				"IBLow": 40000.50				
			}
            "TSLStepSize": 0.5,
            "SignalEntry": {
                "Option": BANKNIFTY06Jul2319100CE,
                "Event": "Bullish-MediumIB-IBLowDowncross",
				"EntryTime": 10:45:29AM,
				"EntryPrice": 185.50,
                "ExitTime": 03:12:22PM,
                "ExitPrice": 159.45			
			},
		},
		{
			"name": "FinNifty",
			"token": 257801,
			"NextExpiry": "04Jul23",
			"InstruMood": "Bullish",
            "OptionRegime": "Buy", #Manual
			"InTrade": false,
			"CompletedTrades": 0,
            "WeekdayPrcRef": {
                "Mon": 18,
				"Tue": 21,
				"Wed": 24,
				"Thu": 25,
				"Fri": 15
            },
            "ATR5D": 118.00,
            "IBValue": 65.00,
            "IBLevel": "Big",
			"TriggerPoints": {
				"IBHigh": 19072.50,
				"IBLow": 19015.50				
			}
            "TSLStepSize": 0.5,
            "SignalEntry": {
                "Option": NIFTY06Jul2319100CE,
                "Event": "Bullish-MediumIB-IBHighUpcross",
				"EntryTime": 10:45:29AM,
				"EntryPrice": 85.50,
                "ExitTime": 03:12:22PM,
                "ExitPrice": 159.45			
			},
		}
	]
}

############################ brokers.json ###########################
{
    "zerodha": {
        "omkar": {
            "username": "YY0222", #Fixed
            "password": "K@nnada444", #Fixed
            "api_key": "6b0dp5ussukmo67h", #Fixed
            "api_secret": "eln2qrqob5neowjuedmbv0f0hzq6lhby", #Fixed
            "totp": "3GN2DNUD35FZQDIIWJUK6CSUIWBPXSYJ", #Fixed
            "access_token": "fjsZXTgy57DACeDjw8jh2DDmXfb90AYv", #Updated Daily (9:05 AM)
            "current_capital": 1009000.00, #Updated Daily (9:05 AM)
            "percentageRisk": {
                "AmiPy": {
                    "riskPerc": 1.5  #Manual                 
                },
                "MPWizard": {
                    "riskPerc": 1.5, #Manual
                    "SignalEntry": {
                        "Option": "NIFTY06Jul2319100CE",
                        "Event": "Bullish-MediumIB-IBHighUpcross",
                        "EntryTime": "10:45:29AM",
                        "EntryPrice": 85.50,
                        "ExitTime": "03:12:22PM",
                        "ExitPrice": 159.45,
                        "PeakMargin": 85000.00,		
                    } # Updated every minute
            }
            }
        }
    },
    "aliceblue": {
        "vimala": {
            "username": "BY1424",
            "password": "K@nnada333",
            "twoFA": "1963",
            "api_secret": "a9bkSpfZn6x24iWvh1L8epG464l2OqZJIpc4gzWOOmKSacMCtmZtTn8W328rqd1KVzDBPP3M50Frhy0cCnCk272E1z1CrosIAlTD",
            "app_code": "mqTi31aA56ylUKh",
            "api_key": "yn6YMylMSOa7Qmp9OPYhtFWSE4OL7hTMTIptvx1Odl1DkVOxqCFuboLnTCJiEd2IoEQolWY7G1JlABIkPxsvDL81hcAcOa08zszFj7DFgqPkNKGJAll3tP3OZjvmIYH6",
            "totp_access": "LELYLKNKQBYKQFYGUPNJHMDDERGAGBWF",
            "session_id": "YfCsNizfGJ2YelpgFQDol1HvG4G5HBjTDgUvZrDMTHRJ4VDdHO3PibmCxmI8xAfikKvyHCaZSjKQfeDKFcSdkzcPe0jagLmXTf8iyWVoQnvfZk3juXLb4SI0AcQU0gp0XQLxXRkrAcp0x6CMT1uhglFSu5XH2iXk5XCOil8hRki4HqQQPOAHJyuvY2EOUMUNZqnOfmiQXmidCtr6zWYUeyJ3j9k7NejG0UGCBF6bz7uiFeG3MblOXdJDz7fP41vz",
            "current_capital": 179000.00,
            "percentageRisk": {
                "MPWizard": {
                    "riskPerc": 1.5,
                    "SignalEntry": {
                        "Option": "NIFTY06Jul2319100CE",
                        "Event": "Bullish-MediumIB-IBHighUpcross",
                        "EntryTime": "10:45:29AM",
                        "EntryPrice": 85.50,
                        "ExitTime": "03:12:22PM",
                        "ExitPrice": 159.45,
                        "PeakMargin": 65000.00,			
                    }
            }
            }
        },
        "venkatesh": {
            "username": "924446",
            "password": "K@nnada444",
            "twoFA": "1991",
            "api_secret": "pyNZQITYOntcNgJfybPnjnzLCSWySWekJyIdWArllibJodoOUAZguBKBlmBZIhclcunfktVvuUpFsSGqoppQjPRiHVFRXMlfJPMx",
            "app_code": "RPMGgKDNcqpdXtM",
            "api_key": "guei1IQcY13sT7gb4ofiTNHBsQ7pJrPuhmJEZXlRRKdMm6xpRWTCGAUGB0yDir7yWQI7aIendjvybuVzeWIzS5nP9JJKMQY1Q1XYzzPS8FCsb908VzPiihY1VnYeZHeV",
            "totp_access": "JDPHMIKEPJERXYLFKDNFBVLIEKOTIQYX",
            "session_id": "YSkCgUJDmZ69BVZnEkR3PoVF16dgYWMV2WbtMfgLBJ5rVnEbfEGR5Hjizt6BrYBXgve83RS5LvIZVrIzfxK97J4UhFsX4dGmKOpRN3ZLshp3Odot2EV0UPLsqdz4cx5Uy1C8YDj8OiuB9dkQpMriLBuNU69mkTLn0qWMehNW46IbIAHrCzRDp1ujxcFEphg7cM6kHmAxsC1hiKH5hr2bfSMZs4BQx0TGLOcLHWyvgxCE89gSZVv9TectUZacCVVU",
            "current_capital": 81000.00,
            "percentageRisk": {
                "MPWizard": {
                    "riskPerc": 1.5,
                    "SignalEntry": {
                        "Option": "NIFTY06Jul2319100CE",
                        "Event": "Bullish-MediumIB-IBHighUpcross",
                        "EntryTime": "10:45:29AM",
                        "EntryPrice": 85.50,
                        "ExitTime": "03:12:22PM",
                        "ExitPrice": 159.45,
                        "PeakMargin": 65000.00,			
                    }
            }
            }
        },
        "sridhar": {
            "username": "935347",
            "password": "K@nnada333",
            "twoFA": "1990",
            "api_secret": "zmOAKJMzMpTKtuNNvPeRKHIWVKFFidIjyMcWxQgAgQVofznoPQzfZtzakSYIiWZmhyhtONSfTsUfmHAcRxVayQUymMLkrqfvGRdd",
            "app_code": "HaRYaumJCQuFiEy",
            "api_key": "pjILfdi8AR80eKFImLVa7g6snJg1tRhsiIqj4BigYLNe4sdYBgsElQi2tj58Q9h84SlGtD1Vd1HVeD5V3FP0VQnlAbp0jfSrdcUsoLIDP8gTNLDuCucOOioysV50Dhxc",
            "totp_access": "LLVHRECRLXBEXEFDREHVSOFFJFLDISZO",
            "session_id": "XG9Sums4Pfk7CgjTbNhD2D0o5KAVXnJ8bk1ZgnGONbjzulLzqpmKZTAJmDa0u9emnzMfO95sTFyFpFbrLtPJcpADYJVhtS7JBuKHaLTdJZuxOlgHGCH9D004cmKkVqnpN1kKuOB26bkISDAzkzKRz3GATT2vAOE2HlOJWmh75oSDUApH0rWfi69y6Em2TsAvLQcXOfjOfzWnJcESFdVLOQ0x7kpmZZinqaxJ3s9CkcPFqIUMRiYGR5l3Bq4H96ki",
            "current_capital": 40000.00,
            "percentageRisk": {                
                "MPWizard": {
                    "riskPerc": 1.5,
                    "SignalEntry": {
                        "Option": "NIFTY06Jul2319100CE",
                        "Event": "Bullish-MediumIB-IBHighUpcross",
                        "EntryTime": "10:45:29AM",
                        "EntryPrice": 85.50,
                        "ExitTime": "03:12:22PM",
                        "ExitPrice": 159.45.
                        "PeakMargin": 65000.00,			
                    }
            }
            }
        },
        "vinay": {
            "username": "935325",
            "password": "K@nnada333",
            "twoFA": "1987",
            "api_secret": "GaHGHkoJMHOmclfFtBpsxFfCmftNaUbHhVWPrZZbeYIvarcIaTVhYJVZTRCAEcyCqbOTBdENgzENdtOWgrmJDPoevURyNISZeRaE",
            "app_code": "kKThxMchucTIuEs",
            "api_key": "xk0s3ZYuDK4K9hAlFErG68J5enGIEbajbmNxcYAJp0opPLofEFABilIh6LDn9oDtavhJ3NKarJLaVAmcIPZcxSCMMWITxBNFgPl1nNlQIUV7hqtnAzfbeife4DnZQHC7",
            "totp_access": "HYUHYOKAUBPEVZNNIHJLICGHSQNBQQDR",
            "session_id": "rUosn9HqevogALaMv3iUtArIJ1e5VAf7bLHE4KZGhdUF4gUPF4tZjugeLBz2xSnCGkTnb3zHo73vQ28rG2sCqZb96rsjDQuNfgtSN92HWUC82M2RTyz8JW9Tr1Xm1nEFY4O7vdgihW779OtY7taFNNikyl2Td4o6IZgMotPQsfKbkeiJP0lWQCDkUdDGWi7klaVbTmVR0Gsi51zOtPnsUi1nPqOURtuGo1hFeUp00mjX1vepjKKWicoxxnhzEPhu",
            "current_capital": 40000.00,
            "percentageRisk": {
                "AmiPy": {
                    "riskPerc": 1.5                   
                },
                "MPWizard": {
                    "riskPerc": 1.5,
                    "SignalEntry": {
                        "Option": "NIFTY06Jul2319100CE",
                        "Event": "Bullish-MediumIB-IBHighUpcross",
                        "EntryTime": "10:45:29AM",
                        "EntryPrice": 85.50,
                        "ExitTime": "03:12:22PM",
                        "ExitPrice": 159.45,
                        "PeakMargin": 65000.00,			
                    }
            }
            },
        "brijesh": {
            "username": "929016",
            "password": "K@nnada222",
            "twoFA": "1979",
            "api_secret": "dkOINUeJELkqeZMHEvdjI4Eprh8LsXJSBiGGrg7VYSeOh1QTTrTYgo5qjrXVL3iog0jagCJCVemQ5ZGoKw1MfZ4zul6G9aRgKzJG",
            "app_code": "5po56G23CtsPpXU",
            "api_key": "Fsi9p89DqRLXc2CMcqY4TYmH2nN1FpkZP39JztBb40InBCAz7agCZWXqCQqJ4PqxRI8v5UWwvPv3r7lUxlgZqKxt2tYWKm8I8qRiBXyvADw1q9bcTzps3tuwbBfg8BQr",
            "totp_access": "XKNCZMDDCN2ZLHGUHKOHOTWWR6CEI3WF",
            "session_id": "13A0elcM5IAB8ULhDjxkfpr1BmtGhJf1BILrFFYmWL0IsTVPlrcBoKmX5mSdA7JvhCGrXO5sC91GtX8qSmBhJK75Q5u0hX9XZ9BrUIxta9IBBFzge8ItwIjkBKt62Swv47OYFgU57PdZBhR2lLIsOKls99K3v1E6KmSnKtX9A2QzDxlW0QeKwo6C8Wu9JX92xchymQyS5XOYCojq5eI4s0u8Ml3CtVlyUPXzg9jOwzTE4n7UBw",
            "current_capital": 600000.00,
            "percentageRisk": {
                "AmiPy": {
                    "riskPerc": 1.5                   
                },
                "MPWizard": {
                    "riskPerc": 1.5,
                    "SignalEntry": {
                        "Option": "NIFTY06Jul2319100CE",
                        "Event": "Bullish-MediumIB-IBHighUpcross",
                        "EntryTime": "10:45:29AM",
                        "EntryPrice": 85.50,
                        "ExitTime": "03:12:22PM",
                        "ExitPrice": 159.45,
                        "PeakMargin": 65000.00,			
                    }
            }
        }
    }
}}}



