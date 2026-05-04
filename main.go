package main

import (
	"fmt"
	"log"

	"github.com/amarnathcjd/gogram/telegram"
)

func main() {
	client, err := telegram.NewClient(telegram.ClientConfig{
		AppID:        123456,               // 🔴  App ID daal
		AppHash:      "your_app_hash_here", // 🔴  App Hash daal
		MemorySession: true,
	})

	if err != nil {
		log.Fatal(err)
	}

	// Connect to Telegram
	_, err = client.Conn()
	if err != nil {
		log.Fatal(err)
	}

	// Login (OTP + 2FA password agar enabled ho)
	err = client.AuthPrompt()
	if err != nil {
		log.Fatal(err)
	}

	// String session print
	session := client.ExportSession()
	fmt.Println("\n✅ STRING SESSION:\n")
	fmt.Println(session)

	// Account info
	me, err := client.GetMe()
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("\n👤 Logged in as:")
	fmt.Println(client.JSON(me, true))
}
