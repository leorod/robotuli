import { REST, Routes } from 'discord.js';
import 'dotenv/config';
import playSound from './commands/playSound';
import youtube from './commands/youtube';

const handlers = [
    playSound,
	youtube
];
const rest = new REST().setToken(process.env.DISCORD_TOKEN!);

(async () => {
    try {
        const commands = handlers.map(handler => handler.command);
		console.log(`Started refreshing ${commands.length} application (/) commands.`);

		// The put method is used to fully refresh all commands in the guild with the current set
		const data = await rest.put(
			Routes.applicationCommands(process.env.DISCORD_APP_ID!),
			{ body: commands },
		);

		console.log(`Successfully reloaded commands: ${JSON.stringify(data)}`);
	} catch (error) {
		// And of course, make sure you catch and log any errors!
		console.error(error);
	}
})();