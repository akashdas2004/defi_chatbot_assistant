def handle_help():
    return (
        "🧠 Available Commands:\n\n"
        "/market – View top market prices (BTC, ETH, SOL, etc)\n"
        "/summary – View top DeFi vaults and APY\n"
        "/setalert – Get alerts on high APY vaults\n"
        "/myalert – View your current alerts\n"
        "/removealert – Remove an alert\n"
        "/dailyon – Enable daily digest\n"
        "/dailyoff – Disable daily digest\n"
        "/define <term> – Quick DeFi term definition\n"
        "/explain <concept> – Explain DeFi concept using Gemini\n"
        "/logsummary – (admin) Show logs and usage stats\n"
    )