cask "whisperbar" do
  version "1.14.3"
  sha256 "3c993f8001ef8b66c88ae22a4e8655e34c351bd88719e41692c825f7f2b143f2"

  url "https://github.com/kchromik/shoutflow-releases/releases/download/v#{version}/WhisperBar-#{version}.dmg",
      verified: "github.com/kchromik/shoutflow-releases/"

  name "WhisperBar"
  desc "Menu bar speech-to-text powered by whisper.cpp, running entirely on-device"
  homepage "https://whisperbar.app"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on macos: ">= :sequoia"

  app "WhisperBar.app"

  zap trash: [
    "~/Library/Application Support/WhisperBar",
    "~/Library/Caches/com.kchromik.WhisperBar",
    "~/Library/HTTPStorages/com.kchromik.WhisperBar",
    "~/Library/Logs/WhisperBar",
    "~/Library/Preferences/com.kchromik.WhisperBar.plist",
    "~/Library/Saved Application State/com.kchromik.WhisperBar.savedState",
  ]
end
