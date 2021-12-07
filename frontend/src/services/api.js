
var apiHost = 'http://localhost:5000'

export async function getRhymes(language, level, word) {
    return fetch(apiHost + `/rhymes/${language}/${level}/${word}`)
}
