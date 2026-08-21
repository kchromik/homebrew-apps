cask "whisperbar" do
  version "1.18.0"
  sha256 "7e31f155639e56ac9a08438a6b070f571b106281953947330cd1495fde71b549"

  url "https://github.com/kchromik/shoutflow-releases/releases/download/v#{version}/WhisperBar-#{version}.dmg",
      verified: "github.com/kchromik/shoutflow-releases/"
  name "WhisperBar"
  desc "Menu bar speech-to-text powered by whisper.cpp, running entirely on-device"
  homepage "https://whisperbar.app/"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on macos: :sequoia

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
