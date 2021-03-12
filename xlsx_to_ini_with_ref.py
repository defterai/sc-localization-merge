#!/usr/bin/python

# Convert global.ini.xlsx & global_ref.ini => global.ini

import sys
from localization import * 

versionFormat = ' - v{0}'
versionAddKeys = set(['pause_ForegroundMainMenuScreenName'])
allowOutdatedTranslationUse = True
excludeTranslateKeys = set(['mobiGlas_ui_notification_Party_Title'])

def compareFormats(refValue, origValue):
    refFormats = LocalizationIni.GetUnnamedFormats(refValue)
    origFormats = LocalizationIni.GetUnnamedFormats(origValue)
    if refFormats != origFormats:
        return False
    refFormats = LocalizationIni.GetNamedFormats(refValue)
    origFormats = LocalizationIni.GetNamedFormats(origValue)
    if refFormats != origFormats:
        return False
    return True

def threeWayMerge(key, refValue, origValue, translateValue):
    if (refValue == origValue):
        return translateValue
    if allowOutdatedTranslationUse and compareFormats(refValue, origValue):
        print("Note: outdated translation key used: ", key)
        return translateValue
    print("Note: reference key used: ", key)
    return refValue

def isTranslatableKey(key):
    return key not in excludeTranslateKeys

def main(args):
    if len(args) < 5:
        print('Error: Wrong script parameters')
        return 1
    try:
        outputFilename = args[1]
        referenceIniFilename = args[2]
        version = args[3] if args[3] != "none" else None
        inputFilenames = args[4:]
        print("Convert ini to xsls (with ref {2}): {0} -> {1}".format(inputFilenames, outputFilename, referenceIniFilename))
        verifyOptions = { 'allowed_characters_file': 'allowed_codepoints.txt' }
        print("Process reference ini...")
        LocalizationIni.SetEnableParseExceptions(True);
        referenceIni = LocalizationIni.FromIniFile(referenceIniFilename)
        print("Reference keys: {0}".format(referenceIni.getItemsCount()))
        print("Process xlsx...")
        inputInis = LocalizationIni.FromXlsxFiles(inputFilenames, 2)
        originalIni = inputInis[0];
        translateIni = inputInis[1];
        if originalIni.getItemsCount() > 0:
            print("Translated keys: {0}/{1} ({2:.2f}%)".format(translateIni.getItemsCount(), originalIni.getItemsCount(),
                                                               translateIni.getItemsCount() / originalIni.getItemsCount() * 100))
            print("           left: {0}".format(originalIni.getItemsCount() - translateIni.getItemsCount()))
        VerifyTranslationIni(originalIni, translateIni, verifyOptions)
        print("Write output...")
        outputIni = LocalizationIni.Empty()
        for key, value in referenceIni.getItems():
            writeValue = value
            if translateIni.isContainKey(key) and isTranslatableKey(key):
                writeValue = threeWayMerge(key, value, originalIni.getKeyValue(key), translateIni.getKeyValue(key))
            if version and (key in versionAddKeys):
                writeValue = writeValue + versionFormat.format(version)
                print("Info: Added version to key: {0}".format(key))
            outputIni.putKeyValue(key, writeValue)
        outputIni.saveToIniFile(outputFilename)
    except KeyboardInterrupt:
        print("Interrupted")
        return 1
    except Exception as err:
        print("Error: {0}".format(err))
        return 1
    print('Done')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
