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

	fmt.Print("Enter your App ID (from my.telegram.org): ")
	appIDStr, _ := reader.ReadString('\n')
	appIDStr = strings.TrimSpace(appIDStr)

	appID64, err := strconv.ParseInt(appIDStr, 10, 32)
	if err != nil || appID64 <= 0 {
		log.Fatal("❌  Invalid App ID. Must be a positive integer (e.g. 12345678).")
	}
	appID := int32(appID64)

	fmt.Print("Enter your App Hash (from my.telegram.org): ")
	appHash, _ := reader.ReadString('\n')
	appHash = strings.TrimSpace(appHash)
	if len(appHash) < 10 {
		log.Fatal("❌  App Hash looks invalid. Should be a 32-character hex string.")
	}

	fmt.Println()
	fmt.Println("🔗  Connecting to Telegram …")

	client, err := telegram.NewClient(telegram.ClientConfig{
		AppID:         appID,
		AppHash:       appHash,
		MemorySession: true,
		LogLevel:      telegram.LogError,
	})
	if err != nil {
		log.Fatalf("❌  Failed to create client: %v", err)
	}

	_, err = client.Conn()
	if err != nil {
		log.Fatalf("❌  Failed to connect: %v", err)
	}
	fmt.Println("✅  Connected!")
	fmt.Println()

	err = client.AuthPrompt()
	if err != nil {
		log.Fatalf("❌  Login failed: %v", err)
	}

	session := client.ExportSession()

	fmt.Println()
	fmt.Println("╔══════════════════════════════════════════╗")
	fmt.Println("║       ✅  YOUR STRING SESSION  ✅        ║")
	fmt.Println("╚══════════════════════════════════════════╝")
	fmt.Println()
	fmt.Println(session)
	fmt.Println()

	const outFile = "session_string.txt"
	if werr := os.WriteFile(outFile, []byte(session+"\n"), 0600); werr != nil {
		fmt.Printf("⚠️   Could not save session to file: %v\n", werr)
	} else {
		fmt.Printf("💾  Session saved to: %s\n", outFile)
	}

	me, err := client.GetMe()
	if err != nil {
		fmt.Printf("⚠️   Could not fetch account info: %v\n", err)
		return
	}

	fmt.Println()
	fmt.Println("👤  Logged in as:")
	fmt.Println(client.JSON(me, true))
	fmt.Println()
	fmt.Println("⚠️   KEEP YOUR SESSION STRING SECRET — it gives full access to your account!")
}

func printBanner() {
	fmt.Println("╔══════════════════════════════════════════╗")
	fmt.Println("║  Telegram String Session Generator       ║")
	fmt.Println("║  Powered by GoGram                       ║")
	fmt.Println("║  github.com/amarnathcjd/gogram           ║")
	fmt.Println("╚══════════════════════════════════════════╝")
	fmt.Println()
	fmt.Println("Get your API credentials at: https://my.telegram.org/apps")
	fmt.Println()
}
