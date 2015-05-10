#!/bin/bash

echo ""
echo "Copying the following files from UVic Individual Temp storage:"
echo ""

ls -h /Volumes/uvindtemp/s/sahoward/workspace-OSX;

echo ""

cp -r /Volumes/uvindtemp/s/sahoward/workspace-OSX/* ~/Desktop;

echo "Finished copying.  Now customizing Mac OS X settings..."
echo ""
# Disable the "are you sure you want to open this file" dialog
xattr -d -r com.apple.quarantine ~/Desktop

###############################################################################
# General UI/UX                                                               #
###############################################################################

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


echo ""
echo "Opening Chromium, please immediately set as default browser."
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/Chromium.zip
open ~/Desktop/Chromium.app/Contents/MacOS/Chromium
sleep 15
~/Desktop/Chromium.app/Contents/MacOS/Chromium ~/Desktop/extensions/crx/*
echo "Done."
echo ""
sleep 30


echo ""
echo "Opening iTerm2 and installing colour schemes."
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/iTerm.zip
~/Desktop/iTerm.app/Contents/MacOS/iTerm ~/Desktop/extensions/colours/*
echo "Done."
echo ""


echo ""
echo "Installing and patching Sublime Text 3."
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/SublimeText.zip
sleep 5
#open ~/Desktop/SublimeText-patch.zip
open ~/Desktop/Sublime\ Text.app/Contents/MacOS/Sublime\ Text
chmod u+x ~/Desktop/extensions/subl/Sublime\ Text
sleep 5
killall Sublime\ Text
cp ~/Desktop/extensions/subl/Sublime\ Text ~/Desktop/Sublime\ Text.app/Contents/MacOS/Sublime\ Text
sleep 2
open ~/Desktop/Sublime\ Text.app/Contents/MacOS/Sublime\ Text
# add the "subl" terminal launch shortcut
ln -s ~/Desktop/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl
# rm ~/Desktop/Sublime\ Text.zip ~/Desktop/Sublime\ Text\ patch.zip ~/Desktop/Sublime\ Text
echo "Done."
echo ""


echo ""
echo "Installing F.lux"
echo ""
cd ~/Desktop
unzip -o ~/Desktop/Flux.zip
open Flux.app/Contents/MacOS/Flux
# rm ~/Desktop/Flux.zip
echo "Done."
echo ""

echo ""
echo "Installing Spotify"
echo ""
cd ~/Desktop
unzip -oq ~/Desktop/SpotifyInstaller.zip
open ~/Desktop/Install\ Spotify\ OSX.app/
# rm ~/Desktop/Install\ Spotify\ OSX.zip
echo "Done."
echo ""

# cleanup zip files
rm -r ~/Desktop/*.zip

echo "Mac setup is complete.  Enjoy."