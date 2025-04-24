import { AudioPlayerStatus, createAudioPlayer, createAudioResource, joinVoiceChannel, StreamType, VoiceConnection, VoiceConnectionStatus } from "@discordjs/voice";
import { Guild, VoiceBasedChannel } from "discord.js";
import fs from 'fs';
import Stream from "stream";

export default class VoiceAgent {
    private channel: VoiceBasedChannel;
    private guild: Guild;
    private connection?: VoiceConnection;

    constructor(channel: VoiceBasedChannel, guild: Guild) {
        this.channel = channel;
        this.guild = guild;
    }

    public play(stream: Stream.Readable) {
        const resource = createAudioResource(stream);
        const player = createAudioPlayer();
        player.play(resource);
        this.connection?.subscribe(player);
        player.on(AudioPlayerStatus.Idle, () => {
            console.log(`Finished playing audio @ ${this.channel.name}`);
            player.stop();
        });
    }

    public join(): VoiceConnection {
        this.connection = joinVoiceChannel({
            channelId: this.channel.id,
            guildId: this.guild.id,
            adapterCreator: this.guild.voiceAdapterCreator
        });
        this.connection.on(VoiceConnectionStatus.Ready, () => {
            console.log(`Joined voice channel: ${this.channel.name} @ ${this.guild.name}`);
        });

        return this.connection;
    }
}