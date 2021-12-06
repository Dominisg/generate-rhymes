import * as Axios from 'axios'

var apiHost = 'http://localhost:5000'

const api = Axios.create({
    baseURL: apiHost,
    headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
    }
})

export async function getRhymes(language, level, word) {
    return api.get(`/rhymes/${language}/${level}/${word}`)
}
