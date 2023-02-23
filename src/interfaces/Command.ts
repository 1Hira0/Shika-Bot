import {
    SlashCommandBuilder,
    SlashCommandSubcommandsOnlyBuilder,
  } from 'discord.js';
  import { CommandInteraction } from "discord.js";
  
  export interface Command {
    data:
      | Omit<SlashCommandBuilder, "addSubcommandGroup" | "addSubcommand">
      | SlashCommandSubcommandsOnlyBuilder;
    run: (interaction: CommandInteraction) => Promise<void>;
  }