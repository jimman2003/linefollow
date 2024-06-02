# Linefollower 
![RPI Pico](https://img.shields.io/badge/Built%20on%20Raspberry%20Pi%20Pico-A22846?style=for-the-badge&logo=RaspberryPi&logoColor=white) <br>
![Pico SDK](https://img.shields.io/badge/BUILT%20WITH%20PICO%20SDK-3178C6?style=flat&logo=c&logoColor=white)

# Περιγραφή Project
Το ρομπότ μας χρησιμοποιεί Raspberry Pi Pico W και Maker Drive. Για την τροφοδοσία του
χρησιμοποιείται μία μπαταρία λιθίου 18650 των 3,7V. Διαθέτει επίσης διακόπτη ON/OFF.
Tο αμάξωμά του είναι φτιαγμένο από χαρτόνι και κολλητική ταινία. Οι ρόδες έχουν υποστεί
μεταποίηση και έχουν διευρυνθεί σε πλάτος και σε μήκος διαμέτρου. Επίσης το ρομπότ μας
χρησιμοποιεί τον Maker Line αισθητήρα ο οποίος διαθέτει 5 ψηφιακές και μία αναλογική
έξοδο. <br>
Για τις ανάγκες του Project δεν χρησιμοποιήθηκε η αναλογική έξοδος.
### Εικόνες:
<img width="406" alt="image" src="https://github.com/jimman2003/linefollow/assets/94703285/f1288ec9-4784-4b41-980f-c24cc8720000">

[3D Scan](https://poly.cam/capture/489058ac-1754-440b-abd4-46fbd2f806c1)
 

## Αρχεία
### [```C/linefollow.c```](C/linefollow.c): Σε αυτό το αρχείο βρίσκεται το κύριο πρόγραμμα. <br>

### [```C/motor_driver.c/.h```](C/motor_driver.c): Βιβλιοθήκη για την λειτουργία των κινητήρων <br>

### [```C/CMakeLists.txt```](C/CMakeLists.txt): Οδηγίες για τον compiler 

### [```C/pico_sdk_import.cmake```](C/pico_sdk_import.cmake): Βιβλιοθήκη για τον RP2040 

# Build Instructions
```
mkdir build
cd build
cmake ..
```

