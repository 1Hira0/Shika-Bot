import fetch from "node-fetch";

export async function getDominantColour(url:String) {
    const res = await fetch(`
        https://api.sightengine.com/1.0/check.json?api_user=${process.env.SUSER}&api_secret=${process.env.SKEY}&url=${url}&models=properties`, {
        method: "GET"})
    const colors = await res.json()
    return colors.colors.dominant.hex
}