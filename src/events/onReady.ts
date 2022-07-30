import { REST } from "@discordjs/rest";
import { Routes } from "discord-api-types/v9";
import { Client } from "discord.js";
import { CommandList } from "../commands/_CommandList";

export const onReady = async (BOT: Client) => {
  const rest = new REST({ version: "9" }).setToken(
    process.env.BOT_TOKEN as string
  );

  const commandData = CommandList.map((command) => command.data.toJSON());

  await rest.put(
    Routes.applicationCommands(
      BOT.user?.id || "missing id"//,
      //process.env.GUILD_ID as string
    ),
    { body: commandData }
  );

  console.log(`Connected with js as ${BOT.user?.username} `);
};