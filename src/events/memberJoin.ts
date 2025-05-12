import { GuildMember, TextChannel } from "discord.js";

export const onMemberJoin = async (guy: GuildMember) => {
    if (guy.guild.id == "1370062593603010621") {
        guy.roles.add("1370073421504839690")
        const c = await guy.guild.channels.fetch("1370072981656571995") as TextChannel
        const m = c.send(`Hello there <@${guy.id}>! Please wait for mods to add your roles`)
    }
};