import { randomUUID } from 'crypto';
import { ChatInputCommandInteraction, Interaction, SharedSlashCommandOptions, SlashCommandBuilder, SlashCommandOptionsOnlyBuilder } from 'discord.js';
import fs from 'fs';
import path from 'path';
import ytdl, { getURLVideoID } from 'ytdl-core';

const cache: { [videoId: string]: string } = {};

const command = new SlashCommandBuilder()
    .setName('yt')
    .setDescription('Reproducir de YouTube')
    .addStringOption(option => option.setName('url')
        .setDescription('URL')
        .setRequired(true));

export default {
    command,
    execute: (interaction: ChatInputCommandInteraction) => {
        const url = interaction.options.getString('url');
        const videoId = getURLVideoID(url!);
        let filename = cache[videoId];
        if (!filename) {
            filename = `${randomUUID()}.mp3`;
            const stream = ytdl(url!, { filter: 'audioonly' });
            stream.pipe(fs.createWriteStream(filename))
                .on('finish', () => {
                    cache[videoId] = filename;
                });
            return stream;
        } else {
            return fs.createReadStream(filename);
        }
    }
}