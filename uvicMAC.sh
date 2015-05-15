#!/bin/bash

# #download dmg
# curl -LOC - http://foo.bar/file.ext

# #mount
# hdiutil mount cotvnc-20b4.dmg

# #copy the app
# sudo cp -R "/Volumes/Chicken of the VNC/Chicken of the VNC.app" /Applications
# #OR
# #install the package
# sudo installer -package /path/to/package -target "/Volumes/Macintosh HD"

# #eject dmg
# cd ~
# hdiutil unmount "/Volumes/Chicken of the VNC/"

#to download shortened url:
#curl -L -o newname.ext http://your.shortened.url

# Find most recent (first listed) chromium version from http://sourceforge.net/projects/osxportableapps/files/Chromium/ and download with curl, open and copy to desktop, then discard dmg.



# from homebrew cask for chromium:

#!/bin/bash
# chromium_version = '42.0.2311.90'
#  # sourceforge.net is the official download host per the vendor homepage
# chromium_url = "http://downloads.sourceforge.net/sourceforge/osxportableapps/Chromium_OSX_#{chromium_version}.dmg"

# iTerm: https://iterm2.com/downloads/stable/iTerm2_v2_0.zip
# SublimeText: http://c758482.r82.cf2.rackcdn.com/Sublime%20Text%20Build%203083.dmg



echo ""
echo "THIS WILL DELETE ALL FILES FROM THE DESKTOP!!"
sleep 3
echo ""
echo ""
echo "Press control-C to cancel this operation and preserve current desktop."
echo ""
echo "Countdown to desktop cleanup:"
for i in {10..1}
do
   echo "$i"
   sleep 1
done

rm -rf /Users/sahoward/Desktop/*
rm -rf /Users/sahoward/Desktop/.*
rm -rf /Users/sahoward/Desktop/_*

echo ""
echo "Copying the following files from UVic Individual Temp storage:"
echo ""

ls -h /Volumes/uvindtemp/s/sahoward/workspace-OSX;

echo ""

ln -s /Volumes/uvindtemp/s/sahoward/ ~/Desktop/sahoward
cp -r /Volumes/uvindtemp/s/sahoward/workspace-OSX/* ~/Desktop;

echo "Finished copying.  Now customizing Mac OS X settings..."
echo ""


###############################################################################
# General UI/UX                                                               #
###############################################################################

# Disable the "are you sure you want to open this file" dialog for apps on Desktop
xattr -d -r com.apple.quarantine ~/Desktop 

# Set a blazingly fast keyboard repeat rate
defaults write NSGlobalDomain KeyRepeat -int 0

# Increase window resize speed for Cocoa applications
defaults write NSGlobalDomain NSWindowResizeTime -float 0.001

# Expand save panel by default
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true

# Finder: show path bar
defaults write com.apple.finder ShowPathbar -bool true

# Finder: allow text selection in Quick Look
defaults write com.apple.finder QLEnableTextSelection -bool true

# Display full POSIX path as Finder window title
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true

# Change default shell to zsh
echo "export SHELL=/bin/zsh" >> ~/.bash_profile;
echo "exec /bin/zsh -l" >> ~/.bash_profile
echo "alias backup='rm -rf /Volumes/uvindtemp/s/sahoward/workspace-OSX/extensions/crx/; mkdir /Volumes/uvindtemp/s/sahoward/workspace-OSX/extensions/crx;  cp -r /Users/sahoward/Library/Application\ Support/Chromium/Default/* /Volumes/uvindtemp/s/sahoward/workspace-OSX/extensions/crx/'" >> ~/.bash_profile 
 
# Enable Text Selection in Quick Look Windows
defaults write com.apple.finder QLEnableTextSelection -bool TRUE
killall Finder
 
# Always Show the User Library Folder
chflags nohidden ~/Library/
 
# Remove shadow from screenshot
defaults write com.apple.screencapture disable-shadow -bool true;killall SystemUIServer

# Show Only Currently Active Apps in the Mac OS X Dock
defaults write com.apple.dock static-only -bool TRUE

###############################################################################
# Dock, Dashboard, and hot corners                                            #
###############################################################################

# Wipe all (default) app icons from the Dock
# This is only really useful when setting up a new Mac, or if you don’t use
# the Dock to launch apps.
defaults write com.apple.dock persistent-apps -array

# Enable highlight hover effect for the grid view of a stack (Dock)
defaults write com.apple.dock mouse-over-hilite-stack -bool true

# Set the icon size of Dock items to 48 pixels
defaults write com.apple.dock tilesize -int 48

# Change minimize/maximize window effect
defaults write com.apple.dock mineffect -string "scale"

# Minimize windows into their application’s icon
defaults write com.apple.dock minimize-to-application -bool true

# Enable spring loading for all Dock items
defaults write com.apple.dock enable-spring-load-actions-on-all-items -bool true

# Show indicator lights for open applications in the Dock
defaults write com.apple.dock show-process-indicators -bool true



###############################################################################
# Applications                                                                #
###############################################################################

####################################
# Chromium
####################################

echo ""
echo "Opening Chromium, please immediately set as default browser."
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/Chromium.zip
cp -r /Volumes/uvindtemp/s/sahoward/workspace-OSX/extensions/crx/* /Users/sahoward/Library/Application Support/Chromium/Default/ &
wait %1
open ~/Desktop/Chromium.app/Contents/MacOS/Chromium

####################################
# iTerm
####################################

echo ""
echo "Opening iTerm2 and installing colour schemes."
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/iTerm.zip & 
wait %1
open ~/Desktop/iTerm.app/Contents/MacOS/iTerm 
# Install preferences
~/Desktop/iTerm.app/Contents/MacOS/iTerm ~/Desktop/extensions/iterm/com.* & 
wait %1
# Install colour schemes
FILES=/Users/sahoward/Desktop/extensions/iterm/*.itermcolors
for f in $FILES
do
  echo "Installing colour scheme $f..."
  open ~/Desktop/extensions/iterm/*.itermcolors & 
  wait %1
done
echo "Done."
echo ""

####################################
# Sublime Text
####################################

echo ""
echo "Installing and patching Sublime Text 3."
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/SublimeText.zip &
wait %1
open ~/Desktop/Sublime\ Text.app/Contents/MacOS/Sublime\ Text &
wait %1
chmod u+x ~/Desktop/extensions/subl/Sublime\ Text
killall Sublime\ Text
cp ~/Desktop/extensions/subl/Sublime\ Text ~/Desktop/Sublime\ Text.app/Contents/MacOS/Sublime\ Text
# add the "subl" terminal launch shortcut
ln -s ~/Desktop/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl
echo "Done."
echo ""

####################################
# F.lux
####################################

echo ""
echo "Installing F.lux"
echo ""
cd ~/Desktop
unzip -o ~/Desktop/Flux.zip
# open Flux.app/Contents/MacOS/Flux
echo "Done."
echo ""

####################################
# Spotify
####################################

echo ""
echo "Installing Spotify"
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/SpotifyInstaller.zip &
wait %1
open ~/Desktop/Install\ Spotify\ OSX.app/ &
wait %1
echo "Done."
echo ""

####################################
# Cyberduck
####################################

echo ""
echo "Installing Cyberduck"
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/Cyberduck-4.7.zip
echo "Done."
echo ""


# clean up leftover files
rm -r ~/Desktop/*.zip
rm -rf ~/Desktop/_*
# killall Dock Finder iTerm Sublime\ Text Chromium
killall Terminal

echo "Mac setup is complete.  Looks tight. Enjoy."
