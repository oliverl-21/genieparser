import unittest
from unittest.mock import Mock

from pyats.topology import loader, Device
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.junos.show_chassis import ShowChassisFpcDetail,\
                                                 ShowChassisEnvironmentRoutingEngine,\
                                                 ShowChassisFirmware,\
                                                 ShowChassisFirmwareNoForwarding,\
                                                 ShowChassisHardware,\
                                                 ShowChassisHardwareDetail,\
                                                 ShowChassisHardwareDetailNoForwarding,\
                                                 ShowChassisHardwareExtensive,\
                                                 ShowChassisHardwareExtensiveNoForwarding

class TestShowChassisFpcDetail(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': '''
        show chassis fpc detail
        Slot 0 information:
        State                               Online    
        Temperature                      Testing
        Total CPU DRAM                  511 MB
        Total RLDRAM                     10 MB
        Total DDR DRAM                    0 MB
        FIPS Capable                        False 
        FIPS Mode                           False 
        Start time                          2019-08-29 09:09:16 UTC
        Uptime                              208 days, 22 hours, 50 minutes, 26 seconds
    '''}

    golden_parsed_output = {
        "fpc-information": {
        "fpc": {
            "fips-capable": "False",
            "fips-mode": "False",
            "memory-ddr-dram-size": "0",
            "memory-dram-size": "511",
            "memory-rldram-size": "10",
            "slot": "0",
            "start-time": {
                "#text": "2019-08-29 09:09:16 UTC"
            },
            "state": "Online",
            "temperature": {
                "#text": "Testing"
            },
            "up-time": {
                "#text": "208 days, 22 hours, 50 minutes, 26 seconds"
            }
        }
    }
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisFpcDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisFpcDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowChassisEnvironmentRoutingEngine(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': '''
        show chassis environment routing-engine
        Routing Engine 0 status:
        State                      Online Master
    '''}

    golden_parsed_output = {
        "environment-component-information": {
            "environment-component-item": {
                "name": "Routing Engine 0",
                "state": "Online Master"
            }
        }
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisEnvironmentRoutingEngine(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisEnvironmentRoutingEngine(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

class TestShowChassisFirmware(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis firmware
        Part                     Type       Version
        FPC 0                    ROM        PC Bios                                    
                                O/S        Version 19.2R1.8 by builder on 2019-06-21 17:52:23 UTC
    '''}

    golden_parsed_output = {
        "firmware-information": {
            "chassis": {
                "chassis-module": {
                    "firmware": [
                        {
                            "firmware-version": "PC Bios",
                            "type": "ROM"
                        },
                        {
                            "firmware-version": "Version 19.2R1.8 by builder on 2019-06-21 17:52:23 UTC",
                            "type": "O/S"
                        }
                    ],
                    "name": "FPC 0"
                }
            }
        }
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisFirmware(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisFirmware(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowChassisFirmwareNoForwarding(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis firmware no-forwarding
        Part                     Type       Version
        FPC 0                    ROM        PC Bios                                    
                                O/S        Version 19.2R1.8 by builder on 2019-06-21 17:52:23 UTC
    '''}

    golden_parsed_output = {
        "firmware-information": {
            "chassis": {
                "chassis-module": {
                    "firmware": [
                        {
                            "firmware-version": "PC Bios",
                            "type": "ROM"
                        },
                        {
                            "firmware-version": "Version 19.2R1.8 by builder on 2019-06-21 17:52:23 UTC",
                            "type": "O/S"
                        }
                    ],
                    "name": "FPC 0"
                }
            }
        }
        
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisFirmwareNoForwarding(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisFirmwareNoForwarding(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowChassisHardware(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis hardware
        Hardware inventory:
        Item             Version  Part number  Serial number     Description
        Chassis                                VM5D4C6B3599      VMX
        Midplane        
        Routing Engine 0                                         RE-VMX
        CB 0                                                     VMX SCB
        FPC 0                                                    Virtual FPC
          CPU            Rev. 1.0 RIOT-LITE    BUILTIN          
          MIC 0                                                  Virtual
            PIC 0                 BUILTIN      BUILTIN           Virtual
    '''}

    golden_parsed_output = {
        "chassis-inventory": {
            "chassis": {
                "@junos:style": "inventory",
                "chassis-module": [
                    {
                        "name": "Midplane"
                    },
                    {
                        "description": "RE-VMX",
                        "name": "Routing Engine 0"
                    },
                    {
                        "description": "VMX SCB",
                        "name": "CB 0"
                    },
                    {
                        "chassis-sub-module": [
                            {
                                "name": "CPU",
                                "part-number": "RIOT-LITE",
                                "serial-number": "BUILTIN",
                                "version": "Rev. 1.0"
                            },
                            {
                                "chassis-sub-sub-module": {
                                    "description": "Virtual",
                                    "name": "PIC 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                "description": "Virtual",
                                "name": "MIC 0"
                            }
                        ],
                        "description": "Virtual FPC",
                        "name": "FPC 0"
                    }
                ],
                "description": "VMX",
                "name": "Chassis",
                "serial-number": "VM5D4C6B3599"
            }
    }
        
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisHardware(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisHardware(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowChassisHardwareDetail(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis hardware detail
        Hardware inventory:
        Item             Version  Part number  Serial number     Description
        Chassis                                VM5D4C6B3599      VMX
        Midplane        
        Routing Engine 0                                         RE-VMX
          cd0   27649 MB  VMware Virtual IDE Har 00000000000000000001 Hard Disk
        CB 0                                                     VMX SCB
        FPC 0                                                    Virtual FPC
          CPU            Rev. 1.0 RIOT-LITE    BUILTIN          
          MIC 0                                                  Virtual
            PIC 0                 BUILTIN      BUILTIN           Virtual
    '''}

    golden_parsed_output = {
        "chassis-inventory": {
            "chassis": {
                "@junos:style": "inventory",
                "chassis-module": [
                    {
                        "name": "Midplane"
                    },
                    {
                        "chassis-re-disk-module": {
                            "description": "Hard Disk",
                            "disk-size": "27649",
                            "model": "VMware Virtual IDE Har",
                            "name": "cd0",
                            "serial-number": "00000000000000000001"
                        },
                        "description": "RE-VMX",
                        "name": "Routing Engine 0"
                    },
                    {
                        "description": "VMX SCB",
                        "name": "CB 0"
                    },
                    {
                        "chassis-sub-module": [
                            {
                                "name": "CPU",
                                "part-number": "RIOT-LITE",
                                "serial-number": "BUILTIN",
                                "version": "Rev. 1.0"
                            },
                            {
                                "chassis-sub-sub-module": {
                                    "description": "Virtual",
                                    "name": "PIC 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                "description": "Virtual",
                                "name": "MIC 0"
                            }
                        ],
                        "description": "Virtual FPC",
                        "name": "FPC 0"
                    }
                ],
                "description": "VMX",
                "name": "Chassis",
                "serial-number": "VM5D4C6B3599"
            }
        }
        
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisHardwareDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisHardwareDetail(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowChassisHardwareDetailNoForwarding(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis hardware detail no-forwarding
        Hardware inventory:
        Item             Version  Part number  Serial number     Description
        Chassis                                VM5D4C6B3599      VMX
        Midplane        
        Routing Engine 0                                         RE-VMX
          cd0   27649 MB  VMware Virtual IDE Har 00000000000000000001 Hard Disk
        CB 0                                                     VMX SCB
        FPC 0                                                    Virtual FPC
          CPU            Rev. 1.0 RIOT-LITE    BUILTIN          
          MIC 0                                                  Virtual
            PIC 0                 BUILTIN      BUILTIN           Virtual
    '''}

    golden_parsed_output = {
        "chassis-inventory": {
            "chassis": {
                "@junos:style": "inventory",
                "chassis-module": [
                    {
                        "name": "Midplane"
                    },
                    {
                        "chassis-re-disk-module": {
                            "description": "Hard Disk",
                            "disk-size": "27649",
                            "model": "VMware Virtual IDE Har",
                            "name": "cd0",
                            "serial-number": "00000000000000000001"
                        },
                        "description": "RE-VMX",
                        "name": "Routing Engine 0"
                    },
                    {
                        "description": "VMX SCB",
                        "name": "CB 0"
                    },
                    {
                        "chassis-sub-module": [
                            {
                                "name": "CPU",
                                "part-number": "RIOT-LITE",
                                "serial-number": "BUILTIN",
                                "version": "Rev. 1.0"
                            },
                            {
                                "chassis-sub-sub-module": {
                                    "description": "Virtual",
                                    "name": "PIC 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                "description": "Virtual",
                                "name": "MIC 0"
                            }
                        ],
                        "description": "Virtual FPC",
                        "name": "FPC 0"
                    }
                ],
                "description": "VMX",
                "name": "Chassis",
                "serial-number": "VM5D4C6B3599"
            }
        }
        
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisHardwareDetailNoForwarding(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisHardwareDetailNoForwarding(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

class TestShowChassisHardwareExtensive(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis hardware extensive
        Hardware inventory:
        Item             Version  Part number  Serial number     Description
        Chassis                                VM5D4C6B3599      VMX
        Jedec Code:   0x7fb0            EEPROM Version:    0x02
                                        S/N:               VM5D4C6B3599
        Assembly ID:  0x0567            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: VMX                        
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 02 ff 05 67 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 56 4d 35 44 34 43 36 42 33 35 39 39 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Midplane        
        Routing Engine 0                                         RE-VMX
        Jedec Code:   0x0000            EEPROM Version:    0x00
        Assembly ID:  0x0bab            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: RE-VMX                     
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 00 00 00 00 0b ab 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        cd0   27649 MB  VMware Virtual IDE Har 00000000000000000001 Hard Disk
        CB 0                                                     VMX SCB
        Jedec Code:   0x7fb0            EEPROM Version:    0x00
        Assembly ID:  0x0bb5            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: VMX SCB                            
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 00 00 0b b5 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        FPC 0                                                    Virtual FPC
        Jedec Code:   0x7fb0            EEPROM Version:    0x00
        Assembly ID:  0x0baa            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: Virtual FPC                
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 00 00 0b aa 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        CPU            Rev. 1.0 RIOT-LITE    BUILTIN          
        Jedec Code:   0x7fb0            EEPROM Version:    0x02
        P/N:          RIOT-LITE         S/N:               BUILTIN
        Assembly ID:  0xfa4e            Assembly Version:  01.00
        Date:         08-18-2013        Assembly Flags:    0x01
        Version:      Rev. 1.0
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 02 00 fa 4e 01 00 52 65 76 2e 20 31 2e 30
        Address 0x10: 00 00 00 00 52 49 4f 54 2d 4c 49 54 45 00 00 00
        Address 0x20: 42 55 49 4c 54 49 4e 00 00 00 00 00 01 12 08 07
        Address 0x30: dd 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        MIC 0                                                  Virtual
        Jedec Code:   0x0000            EEPROM Version:    0x00
        Assembly ID:  0x0a7d            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: Virtual                    
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 00 00 00 00 0a 7d 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 27 41 0f 08 83 80 f0 86
            PIC 0                 BUILTIN      BUILTIN           Virtual
    '''}

    golden_parsed_output = {
        "chassis-inventory": {
            "chassis": {
                "@junos:style": "inventory",
                "chassis-module": [
                    {
                        "name": "Midplane"
                    },
                    {
                        "chassis-re-disk-module": {
                            "description": "Hard Disk",
                            "disk-size": "27649",
                            "model": "VMware Virtual IDE Har",
                            "name": "cd0",
                            "serial-number": "00000000000000000001"
                        },
                        "description": "RE-VMX",
                        "i2c-information": {
                            "assembly-flags": "0x00",
                            "assembly-identifier": "0x0bab",
                            "assembly-version": "00.00",
                            "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                            "eeprom-version": "0x00",
                            "i2c-data": "Address 0x00: 00 00 00 00 0b ab 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                            "i2c-identifier": "RE-VMX",
                            "i2c-version": None,
                            "jedec-code": "0x0000",
                            "manufacture-date": "00-00-0000",
                            "part-number": None,
                            "serial-number": None
                        },
                        "name": "Routing Engine 0"
                    },
                    {
                        "description": "VMX SCB",
                        "i2c-information": {
                            "assembly-flags": "0x00",
                            "assembly-identifier": "0x0bb5",
                            "assembly-version": "00.00",
                            "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                            "eeprom-version": "0x00",
                            "i2c-data": "Address 0x00: 7f b0 00 00 0b b5 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                            "i2c-identifier": "VMX SCB",
                            "i2c-version": None,
                            "jedec-code": "0x7fb0",
                            "manufacture-date": "00-00-0000",
                            "part-number": None,
                            "serial-number": None
                        },
                        "name": "CB 0"
                    },
                    {
                        "chassis-sub-module": [
                            {
                                "chassis-sub-sub-module": {
                                    "description": "Virtual",
                                    "name": "PIC 0",
                                    "part-number": "BUILTIN",
                                    "serial-number": "BUILTIN"
                                },
                                "description": "Virtual",
                                "i2c-information": {
                                    "assembly-flags": "0x00",
                                    "assembly-identifier": "0x0a7d",
                                    "assembly-version": "00.00",
                                    "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                                    "eeprom-version": "0x00",
                                    "i2c-data": "Address 0x00: 00 00 00 00 0a 7d 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 27 41 0f 08 83 80 f0 86\n                    ",
                                    "i2c-identifier": "Virtual",
                                    "i2c-version": None,
                                    "jedec-code": "0x0000",
                                    "manufacture-date": "00-00-0000",
                                    "part-number": None,
                                    "serial-number": None
                                },
                                "name": "MIC 0"
                            },
                            {
                                "i2c-information": {
                                    "assembly-flags": "0x01",
                                    "assembly-identifier": "0xfa4e",
                                    "assembly-version": "01.00",
                                    "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                                    "eeprom-version": "0x02",
                                    "i2c-data": "Address 0x00: 7f b0 02 00 fa 4e 01 00 52 65 76 2e 20 31 2e 30\n                    Address 0x10: 00 00 00 00 52 49 4f 54 2d 4c 49 54 45 00 00 00\n                    Address 0x20: 42 55 49 4c 54 49 4e 00 00 00 00 00 01 12 08 07\n                    Address 0x30: dd 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                                    "i2c-identifier": None,
                                    "i2c-version": "Rev. 1.0",
                                    "jedec-code": "0x7fb0",
                                    "manufacture-date": "08-18-2013",
                                    "part-number": None,
                                    "serial-number": "BUILTIN"
                                },
                                "name": "CPU",
                                "part-number": "RIOT-LITE",
                                "serial-number": "BUILTIN",
                                "version": "Rev. 1.0"
                            }
                        ],
                        "description": "Virtual FPC",
                        "i2c-information": {
                            "assembly-flags": "0x00",
                            "assembly-identifier": "0x0baa",
                            "assembly-version": "00.00",
                            "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                            "eeprom-version": "0x00",
                            "i2c-data": "Address 0x00: 7f b0 00 00 0b aa 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                            "i2c-identifier": "Virtual FPC",
                            "i2c-version": None,
                            "jedec-code": "0x7fb0",
                            "manufacture-date": "00-00-0000",
                            "part-number": None,
                            "serial-number": None
                        },
                        "name": "FPC 0"
                    }
                ],
                "description": "VMX",
                "i2c-information": {
                    "assembly-flags": "0x00",
                    "assembly-identifier": "0x0567",
                    "assembly-version": "00.00",
                    "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                    "eeprom-version": "0x02",
                    "i2c-data": "Address 0x00: 7f b0 02 ff 05 67 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 56 4d 35 44 34 43 36 42 33 35 39 39 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                    "i2c-identifier": "VMX",
                    "i2c-version": None,
                    "jedec-code": "0x7fb0",
                    "manufacture-date": "00-00-0000",
                    "part-number": None,
                    "serial-number": "VM5D4C6B3599"
                },
                "name": "Chassis",
                "serial-number": "VM5D4C6B3599"
            }
        }
        
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisHardwareExtensive(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisHardwareExtensive(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


class TestShowChassisHardwareExtensiveNoForwarding(unittest.TestCase):

    maxDiff = None

    device = Device(name='test-device')

    empty_output = {'execute.return_value': ''}

    golden_output = {'execute.return_value': 
    ''' show chassis hardware extensive no-forwarding
        Hardware inventory:
        Item             Version  Part number  Serial number     Description
        Chassis                                VM5D4C6B3599      VMX
        Jedec Code:   0x7fb0            EEPROM Version:    0x02
                                        S/N:               VM5D4C6B3599
        Assembly ID:  0x0567            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: VMX                        
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 02 ff 05 67 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 56 4d 35 44 34 43 36 42 33 35 39 39 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Midplane        
        Routing Engine 0                                         RE-VMX
        Jedec Code:   0x0000            EEPROM Version:    0x00
        Assembly ID:  0x0bab            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: RE-VMX                     
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 00 00 00 00 0b ab 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        cd0   27649 MB  VMware Virtual IDE Har 00000000000000000001 Hard Disk
        CB 0                                                     VMX SCB
        Jedec Code:   0x7fb0            EEPROM Version:    0x00
        Assembly ID:  0x0bb5            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: VMX SCB                            
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 00 00 0b b5 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        FPC 0                                                    Virtual FPC
        Jedec Code:   0x7fb0            EEPROM Version:    0x00
        Assembly ID:  0x0baa            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: Virtual FPC                
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 00 00 0b aa 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        CPU            Rev. 1.0 RIOT-LITE    BUILTIN          
        Jedec Code:   0x7fb0            EEPROM Version:    0x02
        P/N:          RIOT-LITE         S/N:               BUILTIN
        Assembly ID:  0xfa4e            Assembly Version:  01.00
        Date:         08-18-2013        Assembly Flags:    0x01
        Version:      Rev. 1.0
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 7f b0 02 00 fa 4e 01 00 52 65 76 2e 20 31 2e 30
        Address 0x10: 00 00 00 00 52 49 4f 54 2d 4c 49 54 45 00 00 00
        Address 0x20: 42 55 49 4c 54 49 4e 00 00 00 00 00 01 12 08 07
        Address 0x30: dd 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        MIC 0                                                  Virtual
        Jedec Code:   0x0000            EEPROM Version:    0x00
        Assembly ID:  0x0a7d            Assembly Version:  00.00
        Date:         00-00-0000        Assembly Flags:    0x00
        ID: Virtual                    
        Board Information Record:
        Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        I2C Hex Data:
        Address 0x00: 00 00 00 00 0a 7d 00 00 00 00 00 00 00 00 00 00
        Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        Address 0x70: 00 00 00 00 00 00 00 00 27 41 0f 08 83 80 f0 86
            PIC 0                 BUILTIN      BUILTIN           Virtual
    '''}

    golden_parsed_output = {
        "chassis-inventory": {
        "chassis": {
            "@junos:style": "inventory",
            "chassis-module": [
                {
                    "name": "Midplane"
                },
                {
                    "chassis-re-disk-module": {
                        "description": "Hard Disk",
                        "disk-size": "27649",
                        "model": "VMware Virtual IDE Har",
                        "name": "cd0",
                        "serial-number": "00000000000000000001"
                    },
                    "description": "RE-VMX",
                    "i2c-information": {
                        "assembly-flags": "0x00",
                        "assembly-identifier": "0x0bab",
                        "assembly-version": "00.00",
                        "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                        "eeprom-version": "0x00",
                        "i2c-data": "Address 0x00: 00 00 00 00 0b ab 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                        "i2c-identifier": "RE-VMX",
                        "i2c-version": None,
                        "jedec-code": "0x0000",
                        "manufacture-date": "00-00-0000",
                        "part-number": None,
                        "serial-number": None
                    },
                    "name": "Routing Engine 0"
                },
                {
                    "description": "VMX SCB",
                    "i2c-information": {
                        "assembly-flags": "0x00",
                        "assembly-identifier": "0x0bb5",
                        "assembly-version": "00.00",
                        "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                        "eeprom-version": "0x00",
                        "i2c-data": "Address 0x00: 7f b0 00 00 0b b5 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                        "i2c-identifier": "VMX SCB",
                        "i2c-version": None,
                        "jedec-code": "0x7fb0",
                        "manufacture-date": "00-00-0000",
                        "part-number": None,
                        "serial-number": None
                    },
                    "name": "CB 0"
                },
                {
                    "chassis-sub-module": [
                        {
                            "chassis-sub-sub-module": {
                                "description": "Virtual",
                                "name": "PIC 0",
                                "part-number": "BUILTIN",
                                "serial-number": "BUILTIN"
                            },
                            "description": "Virtual",
                            "i2c-information": {
                                "assembly-flags": "0x00",
                                "assembly-identifier": "0x0a7d",
                                "assembly-version": "00.00",
                                "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                                "eeprom-version": "0x00",
                                "i2c-data": "Address 0x00: 00 00 00 00 0a 7d 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 27 41 0f 08 83 80 f0 86\n                    ",
                                "i2c-identifier": "Virtual",
                                "i2c-version": None,
                                "jedec-code": "0x0000",
                                "manufacture-date": "00-00-0000",
                                "part-number": None,
                                "serial-number": None
                            },
                            "name": "MIC 0"
                        },
                        {
                            "i2c-information": {
                                "assembly-flags": "0x01",
                                "assembly-identifier": "0xfa4e",
                                "assembly-version": "01.00",
                                "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                                "eeprom-version": "0x02",
                                "i2c-data": "Address 0x00: 7f b0 02 00 fa 4e 01 00 52 65 76 2e 20 31 2e 30\n                    Address 0x10: 00 00 00 00 52 49 4f 54 2d 4c 49 54 45 00 00 00\n                    Address 0x20: 42 55 49 4c 54 49 4e 00 00 00 00 00 01 12 08 07\n                    Address 0x30: dd 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                                "i2c-identifier": None,
                                "i2c-version": "Rev. 1.0",
                                "jedec-code": "0x7fb0",
                                "manufacture-date": "08-18-2013",
                                "part-number": None,
                                "serial-number": "BUILTIN"
                            },
                            "name": "CPU",
                            "part-number": "RIOT-LITE",
                            "serial-number": "BUILTIN",
                            "version": "Rev. 1.0"
                        }
                    ],
                    "description": "Virtual FPC",
                    "i2c-information": {
                        "assembly-flags": "0x00",
                        "assembly-identifier": "0x0baa",
                        "assembly-version": "00.00",
                        "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                        "eeprom-version": "0x00",
                        "i2c-data": "Address 0x00: 7f b0 00 00 0b aa 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                        "i2c-identifier": "Virtual FPC",
                        "i2c-version": None,
                        "jedec-code": "0x7fb0",
                        "manufacture-date": "00-00-0000",
                        "part-number": None,
                        "serial-number": None
                    },
                    "name": "FPC 0"
                }
            ],
            "description": "VMX",
            "i2c-information": {
                "assembly-flags": "0x00",
                "assembly-identifier": "0x0567",
                "assembly-version": "00.00",
                "board-information-record": "Address 0x00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
                "eeprom-version": "0x02",
                "i2c-data": "Address 0x00: 7f b0 02 ff 05 67 00 00 00 00 00 00 00 00 00 00\n                    Address 0x10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x20: 56 4d 35 44 34 43 36 42 33 35 39 39 00 00 00 00\n                    Address 0x30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    Address 0x70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n                    ",
                "i2c-identifier": "VMX",
                "i2c-version": None,
                "jedec-code": "0x7fb0",
                "manufacture-date": "00-00-0000",
                "part-number": None,
                "serial-number": "VM5D4C6B3599"
            },
            "name": "Chassis",
            "serial-number": "VM5D4C6B3599"
        }
    }
        
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowChassisHardwareExtensive(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = ShowChassisHardwareExtensive(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)

if __name__ == '__main__':
    unittest.main()