Primer Ball and Plate sistema za predmet Mehatronika, primenjena elektronika 4. godina.

# Opis primera
Primer obuhvata kompletnu povratnu spregu koja tezi da lopticu dovede i zadrzi na centar ploce.
Postoji kamera koja snima plocu od gore, to je glavni senzor.
Aktuatori su dva motora koja mogu da naginju plocu oko sredine u obe koordinate.

## Webots kontroler kamere
Ovaj kontroler publish-uje ono sto kamera snima kontinualno u formatu slike koji ROS koristi

## ROS node za lokalizaciju loptice
Ovaj ROS Node se Subscribe-uje na topic na koji se objavljuje slika sa kamere, pronalazi poziciju loptice na kameri, a potom objavljuje X i Y koordinatu loptice u odnosu na centar slike

## Kontroler ploce u Webots
Kontroler se pretplacuje na topic o koordinati loptice, a potom na osnovu pozicije loptice PID regulatorom upravlja pozicijama 2 motora.


# Pokretanje primera

Kako biste pokrenuli ovaj primer potrebno je da imate instaliran ROS noetic i instaliran Webots 2022a.

### Webots
Da bi Webots imao pristup ROS bibliotekama, potrebno je otvoriti novi terminal, source-ovati ROS local_setup skriptu:

``` source /opt/ros/noetic/local_setup.bash```

a zatim pokrenuti ```webots``` iz tog terminala.

U Webots-u otvoriti svet iz Worlds direktorijuma.

### ROS core
Otvoriti novi terminal, source-ovati opet ROS i pokrenuti ```roscore```

### Rosnode za obradu slike
U ovom terminalu, sa opet source-ovanim ROS-om, pokrenuti skriptu za analizu slike iz Resources direktorijuma

```python3 find_ball_position.py```
