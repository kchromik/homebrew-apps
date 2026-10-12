cask "whisperbar" do
  version "1.22.1"
  sha256 "7506c71c50d53a93ea33da53f89d46131c4f8dd106815353f70851384fb54e57"

  url "https://github.com/kchromik/shoutflow-releases/releases/download/v#{version}/WhisperBar-#{version}.dmg"
  name "WhisperBar"
  desc "Local speech-to-text and meeting transcription"
  homepage "https://whisperbar.pro/"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
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
