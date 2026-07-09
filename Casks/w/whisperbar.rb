cask "whisperbar" do
  version "1.14.6"
  sha256 "90230b1165f4e0575547176a72eaa70f0469434055ab0f23816fc9567520b4af"

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
