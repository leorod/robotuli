import 'dotenv/config';
import { GatewayIntentBits } from "discord-api-types/v10";
import { Events, Client, ChatInputCommandInteraction, GuildMember } from "discord.js";
import VoiceAgent from './voice/VoiceAgent';
import { resolve } from './commands/commandProcessor';

const agents: { [id: string]: VoiceAgent } = {};

const client = new Client({
  intents: [
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.Guilds,
  ],
});

client.on(Events.ClientReady, () => console.log("Ready!"));

client.on(Events.InteractionCreate, async interaction => {
  if (interaction.isChatInputCommand()) {
    const channelId = (interaction.member as GuildMember).voice.channel?.id;
    if (channelId) {
      const stream = resolve(interaction as ChatInputCommandInteraction);
      if (stream) {
        agents[channelId].play(stream);
      }
    } else {
      await interaction.reply('Llamame al voice capo, si no no puedo');
    }
  }
});

client.on(Events.MessageCreate, async (message) => {
  console.log(`New message; ${message.content}`);
  if (message.content.toLowerCase() === '!join') {
    const channel = message.member?.voice.channel;
    if (channel) {
      const agent = new VoiceAgent(channel, message.guild!);
      agent.join();
      agents[channel.id] = agent;
    } else {
      message.reply('A dónde concha querés que me joinee, cara de pija?');
    }
  }
});

client.on(Events.Error, console.warn);

void client.login(process.env.DISCORD_TOKEN);
