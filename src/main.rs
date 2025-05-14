// Function to modify in main.rs

fn create_config() -> Result<Config, io::Error> {
    let model = loop {
        println!("{}", "Select model:\n 1 for gpt-4o-mini\n 2 for gpt-4o\n 3 for ollama (llama3.1)\n 4 for llamacpp (.gguf model)".cyan());

        io::stdout().flush()?;
        let mut choice = String::new();
        io::stdin().read_line(&mut choice)?;
        match choice.trim() {
            "1" => break Model::OpenAiGpt4o,
            "2" => break Model::OpenAiGpt4oMini,
            "3" => break Model::Ollama("llama3.1".to_string()),
            "4" => {
                // Get model path
                print!("{}", "Enter path to .gguf model file: ".cyan());
                io::stdout().flush()?;
                let mut model_path = String::new();
                io::stdin().read_line(&mut model_path)?;
                let model_path = model_path.trim().to_string();
                
                // Get server URL (default to localhost:8000)
                print!("{}", "Enter server URL (default: http://localhost:8000): ".cyan());
                io::stdout().flush()?;
                let mut server_url = String::new();
                io::stdin().read_line(&mut server_url)?;
                let server_url = if server_url.trim().is_empty() {
                    "http://localhost:8000".to_string()
                } else {
                    server_url.trim().to_string()
                };
                
                break Model::LlamaCpp {
                    model_path,
                    server_url,
                };
            }
            _ => println!("{}", "Invalid choice. Please try again.".red()),
        }
    };

    let max_tokens = loop {
        print!("{}", "Enter max tokens (1-4096): ".cyan());
        io::stdout().flush()?;
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        if let Ok(tokens) = input.trim().parse::<i32>() {
            if tokens > 0 && tokens <= 4096 {
                break tokens;
            }
        }
        println!("{}", "Invalid input. Please enter a number between 1 and 4096.".red());
    };

    Ok(Config {
        model,
        max_tokens,
    })
}