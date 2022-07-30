export const validateEnv = () => {
    if (!process.env.BOT_TOKEN) {
      console.warn("Missing Discord bot token.");
      return false;
    }
}