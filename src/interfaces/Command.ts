import {
    SlashCommandBuilder,
    SlashCommandOptionsOnlyBuilder,
    SlashCommandSubcommandsOnlyBuilder
  } from 'discord.js';
  import { CommandInteraction } from "discord.js";
  
  export interface Command {
    data: SlashCommandBuilder | SlashCommandOptionsOnlyBuilder | SlashCommandSubcommandsOnlyBuilder
    run: (interaction: CommandInteraction) => Promise<void>;
  }