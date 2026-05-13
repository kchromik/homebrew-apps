cask "whisperbar" do
  version "1.14.2"
  sha256 "ad50f853947427d8afda1cae2eb3ecc7ce07e4f6dd3d37cd8128a57cb4b8afcc"

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
