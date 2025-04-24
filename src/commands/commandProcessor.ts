import { ChatInputCommandInteraction, Interaction, SlashCommandBuilder, SlashCommandOptionsOnlyBuilder } from "discord.js";
import playSound from "./playSound";
import Stream from "stream";
import youtube from "./youtube";

export interface CommandHandler {
    command: SlashCommandBuilder | SlashCommandOptionsOnlyBuilder;
    execute: (interaction: ChatInputCommandInteraction) => Stream.Readable | undefined;
}

const handlers: {[name: string]: CommandHandler} = {
    [playSound.command.name]: playSound,
    [youtube.command.name]: youtube
};

export function resolve(interaction: ChatInputCommandInteraction) {
    const handler = handlers[interaction.commandName];
    if (handler) {
        return handler.execute(interaction);
    }
}