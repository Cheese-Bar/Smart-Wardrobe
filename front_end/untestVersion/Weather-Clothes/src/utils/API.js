import Axios from "axios";

const apiKey = "536ab6af7ef7bf09fed9adc314232d23";

export default {
    search: (city) => {
        return Axios.get(
            `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}`)
    }
}