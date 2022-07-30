import { ActivityType, Client, GatewayIntentBits, ApplicationCommandManager } from "discord.js";
import { onInteraction } from "./events/onInteraction";
import { onReady } from "./events/onReady";

console.log("Running");
(async () => {
    const bot = new Client({intents: [GatewayIntentBits.Guilds]});
    bot.on("ready", async () => {await onReady(bot); 
                                bot.user?.setPresence({ activities: [{ type:ActivityType.Playing, name: 'with Discord.js(in ts) + Nextcord' }], status: 'idle' })
                        });
    bot.on("interactionCreate", async (interaction) => await onInteraction(interaction));
    await bot.login(process.env.BOT_TOKEN);
})();