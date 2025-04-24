import { ChatInputCommandInteraction, Interaction, SharedSlashCommandOptions, SlashCommandBuilder, SlashCommandOptionsOnlyBuilder } from 'discord.js';
import fs from 'fs';
import path from 'path';
const SOUNDS_DIR = '../../sounds';

const refMap: {[key: string]: string} = {};

const choices = fs.readdirSync(path.join(__dirname, SOUNDS_DIR))
    .map(filePath => {
        const key = filePath.replace(/^.*\/|\..+?$/, '');
        refMap[key] = filePath;
        return key;
    })
    .map(soundName => ({ name: soundName, value: soundName }));

const command = new SlashCommandBuilder()
        .setName('sound')
        .setDescription('Sonidito')
        .addStringOption(option => option.setName('ref')
            .setDescription('Culo')
            .setRequired(true)
            .addChoices(choices));

export default {
    command,
    execute: (interaction: ChatInputCommandInteraction) => {
        const ref = interaction.options.getString('ref');
        const filePath = path.join(SOUNDS_DIR, ref!);
        if (fs.existsSync(filePath)) {
            return fs.createReadStream(filePath);
        }
    }
}