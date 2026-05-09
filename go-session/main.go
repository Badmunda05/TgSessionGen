package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/amarnathcjd/gogram/telegram"
)

func main() {
	reader := bufio.NewReader(os.Stdin)

	printBanner()

	// ── App ID ───────────────────────────────────────────────
	fmt.Print("Enter your App ID (from my.telegram.org): ")

	appIDStr, _ := reader.ReadString('\n')
	appIDStr = strings.TrimSpace(appIDStr)

	appID64, err := strconv.ParseInt(appIDStr, 10, 32)

	if err != nil || appID64 <= 0 {
		log.Fatal("❌ Invalid App ID. Must be a positive integer.")
	}

	appID := int32(appID64)

	// ── App Hash ─────────────────────────────────────────────
	fmt.Print("Enter your App Hash (from my.telegram.org): ")

	appHash, _ := reader.ReadString('\n')
	appHash = strings.TrimSpace(appHash)

	if len(appHash) < 10 {
		log.Fatal("❌ Invalid App Hash.")
	}

	fmt.Println()
	fmt.Println("🔗 Connecting to Telegram...")

	// ── Create Client ────────────────────────────────────────
	client, err := telegram.NewClient(
		telegram.ClientConfig{
			AppID:         appID,
			AppHash:       appHash,
			MemorySession: true,
			LogLevel:      telegram.LogError,
		},
	)

	if err != nil {
		log.Fatalf("❌ Failed to create client: %v", err)
	}

	_, err = client.Conn()

	if err != nil {
		log.Fatalf("❌ Failed to connect: %v", err)
	}

	fmt.Println("✅ Connected!")
	fmt.Println()

	// ── Login ────────────────────────────────────────────────
	err = client.AuthPrompt()

	if err != nil {
		log.Fatalf("❌ Login failed: %v", err)
	}

	// ── Export Session ───────────────────────────────────────
	session := client.ExportSession()

	fmt.Println()
	fmt.Println("╔══════════════════════════════════════════╗")
	fmt.Println("║       ✅ YOUR STRING SESSION ✅         ║")
	fmt.Println("╚══════════════════════════════════════════╝")
	fmt.Println()

	fmt.Println(session)
	fmt.Println()

	// ── Send Session to Saved Messages ───────────────────────
	message := fmt.Sprintf(
		"✅ YOUR STRING SESSION (GoGram)\n\n<code>%s</code>\n\n⚠️ KEEP YOUR SESSION STRING SECRET!",
		session,
	)

	_, err = client.SendMessage(
		"me",
		message,
		&telegram.SendOptions{
			ParseMode: "html",
		},
	)

	if err != nil {
		fmt.Printf("⚠️ Could not send session to Saved Messages: %v\n", err)
	} else {
		fmt.Println("📨 Session sent to Saved Messages.")
	}

	// ── Account Info ─────────────────────────────────────────
	me, err := client.GetMe()

	if err != nil {
		fmt.Printf("⚠️ Could not fetch account info: %v\n", err)
		return
	}

	fmt.Println()
	fmt.Println("👤 Logged in as:")

	fullName := strings.TrimSpace(
		me.FirstName + " " + me.LastName,
	)

	fmt.Printf("    Name    : %s\n", fullName)

	if me.Username != "" {
		fmt.Printf("    Username: @%s\n", me.Username)
	}

	fmt.Printf("    User ID : %d\n", me.ID)

	if me.Phone != "" {
		fmt.Printf("    Phone   : +%s\n", me.Phone)
	}

	fmt.Println()
	fmt.Println("⚠️ KEEP YOUR SESSION STRING SECRET.")
	fmt.Println("It gives full access to your Telegram account!")
}

func printBanner() {
	fmt.Println("╔══════════════════════════════════════════╗")
	fmt.Println("║  Telegram String Session Generator      ║")
	fmt.Println("║  Powered by GoGram                      ║")
	fmt.Println("╚══════════════════════════════════════════╝")
	fmt.Println()
	fmt.Println("Get your API credentials at:")
	fmt.Println("https://my.telegram.org/apps")
	fmt.Println()
}
