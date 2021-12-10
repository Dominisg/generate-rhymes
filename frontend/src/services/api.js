
var apiHost = 'http://localhost:5000'

export async function getRhymes(language, level, word, inaccurate) {
    if (inaccurate) {
        return fetch(apiHost + `/rhymes/${language}/${level}/${word}?inaccurate`)
    } else {
        return fetch(apiHost + `/rhymes/${language}/${level}/${word}`)
    }
}
