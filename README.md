# Homebrew Tap

Homebrew Cask formulae for WhisperBar.

## Install

Recommended one-liner (trusts and installs only this cask):

```sh
brew install --cask kchromik/apps/whisperbar
```

Or step by step. Since Homebrew 6, casks from third-party taps must be trusted explicitly before they can be installed (see [Tap Trust](https://docs.brew.sh/Tap-Trust)):

```sh
brew tap kchromik/apps
brew trust --cask kchromik/apps/whisperbar
brew install --cask whisperbar
```

## Update

```sh
brew upgrade whisperbar
```

## Uninstall

```sh
brew uninstall whisperbar
```

## About WhisperBar

Fast, private speech-to-text for macOS, powered by whisper.cpp, running entirely on-device.

Learn more at [whisperbar.app](https://whisperbar.app).
