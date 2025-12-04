# iPhonize
A simple Python script to convert Thunderbird \*.vcf files into iOS address book compliant files 

## A brief history
This Python script is a result of "my journey" in Python language: I use Python for some of my academic projects or personal OS management stuffs, so, I decide to study this language in-depth.

One day I have realized that I had many address book in many devices: old backups, old hard disks, old mobile phones... so I decided to create only one address book to update anytime and mirroring it in any devices.

I chose to use the built-in Thunderbird address book but unfortunately I discovered early that my iPhone address book reject the Thunderbird \*.vcf files or import they incorrectly. I  decided to look into the matter and the result is this script that convert the \*.vcf files exported from Thunderbird in a compatible and nice to see \*.vcf file for iPhone.

After the execution of the script the resulting file can be send by email and imported into the iOS address book.

## Usage
Simply run the script with
```
python iPhonize.py
```
A "File open dialog" appear. Select the directory where are the *.vcf files that you wish to convert and click on `Seleziona cartella` or similar (according to localization of your operating system).

For each file in the directory a new file with the same name but ` - iphonize.vcf` suffix will be created.

## Caveats
The instant messaging fields of Thunderbird address book will be skipped.