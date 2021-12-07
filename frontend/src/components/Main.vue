<template>
  <v-contaier fill-height fluid>
    <v-snackbar v-model="snackbar" :multi-line="multiLine" top color="red">
      {{ text }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false"> Close </v-btn>
      </template>
    </v-snackbar>
    <v-row align="center" justify="center" class="mt-10">
      <v-col cols="6">
        <v-row>
          <v-card width="100%">
            <v-form @submit.prevent="generateRhymes">
              <v-card-text>
                <v-row>
                  <v-select
                    :items="languages"
                    label="Language"
                    outlined
                    class="ma-5"
                    v-model="selectedLanguage"
                  ></v-select>
                  <v-text-field
                    label="Word"
                    hide-details="auto"
                    outlined
                    class="ma-5"
                    v-model="enteredWord"
                  ></v-text-field>
                  <v-select
                    :items="levels"
                    label="Level"
                    outlined
                    class="ma-5"
                    v-model="selectedLevel"
                  ></v-select>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-row align="center" justify="center" class="mb-3">
                  <v-btn type="submit" color="green"> Go!</v-btn>
                </v-row>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-row>
        <v-row class="mt-10" align="center" justify="center">
          <Loader v-if="loader" />
          <v-card width="100%" v-if="wordsVisible">
            <v-card-text>
              <v-row align="center" justify="center"> </v-row>
            </v-card-text>
          </v-card>
          <div v-else></div>
        </v-row>
      </v-col>
    </v-row>
    <v-row> </v-row>
  </v-contaier>
</template>

<script>
import { getRhymes } from "@/services/api";
import Loader from "./Loader.vue";
import encoding from "text-encoding";
export default {
  name: "Main",
  components: {
    Loader,
  },
  data: () => ({
    languages: ["English", "Polish"],
    levels: [1, 2, 3, 4],
    selectedLevel: 1,
    selectedLanguage: "English",
    enteredWord: "",
    multiLine: true,
    snackbar: false,
    text: `Word field cannot be empty!`,
    loader: false,
    wordsVisible: false,
  }),

  methods: {
    async generateRhymes() {
      if (this.enteredWord === "") {
        this.snackbar = true;
        return;
      }
      var shortLang;
      switch (this.selectedLanguage) {
        case "English":
          shortLang = "en";
          break;
        case "Polish":
          shortLang = "pl";
          break;
        default:
          break;
      }
      const res = await getRhymes(
        shortLang,
        this.selectedLevel,
        this.enteredWord
      );
      const result = res.body
        .pipeThrough(new encoding.TextDecoderStream())
        .pipeThrough(encoding.splitStream("\n"))
        .pipeThrough(encoding.parseJSON());
      await this.showResults(result.getReader());
    },
    async showResults(reader) {
      reader.read().then(
        ({ value, done }) => {
          if (done) {
            console.log("The stream was already closed!");
          } else {
            console.log(value.word);
            this.showResults(reader);
          }
        },
        (e) =>
          console.error("The stream became errored and cannot be read from!", e)
      );
    },
  },
};
</script>

<style>
</style>