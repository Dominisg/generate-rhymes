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
                  <v-checkbox
                    class="ma-3 mt-12"
                    v-model="inacuurate"
                    label="Inaccurate"
                  >
                  </v-checkbox>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-row align="center" justify="center" class="mb-3">
                  <v-btn
                    type="submit"
                    color="green"
                    :loading="loadingGoButton"
                    class="mr-3"
                  >
                    Go!</v-btn
                  >
                  <v-btn
                    color="green"
                    :disabled="loader || !showMore"
                    :loading="loadingShowMoreButton"
                    @click="showMoreRhymes"
                  >
                    Show More</v-btn
                  >
                </v-row>
              </v-card-actions>
            </v-form>
          </v-card>
        </v-row>
        <v-row class="mt-10" align="center" justify="center">
          <transition name="fade-out-in" mode="out-in">
            <v-row
              align="center"
              justify="center"
              width="100%"
              v-if="wordsVisible"
            >
              <transition-group name="list" tag="p">
                <v-chip
                  class="ma-3"
                  color="#1b4d89"
                  v-for="rhyme in rhymes"
                  :key="rhyme"
                  ><h2 style="color: white">{{ rhyme.word }}</h2></v-chip
                >
              </transition-group>
            </v-row>
            <Loader v-if="loader" />
            <v-row
              align="center"
              justify="center"
              width="100%"
              v-if="noResults"
            >
              <h4 style="color: #7c809b; font-style: italic">
                No rhymes could be found. Try a different word
              </h4>
            </v-row>
          </transition>
        </v-row>
      </v-col>
    </v-row>
    <v-row> </v-row>
  </v-contaier>
</template>

<script>
import { getRhymes } from "@/services/api";
import Loader from "./Loader.vue";
import ndjsonStream from "can-ndjson-stream";
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
    rhymes: [],
    currentReader: 0,
    inacuurate: false,
    currentWordsNumber: 0,
    showMore: false,
    noResults: false,
    loadingGoButton: false,
    loadingShowMoreButton: false,
  }),

  methods: {
    async generateRhymes() {
      this.showMore = false;
      this.rhymes = [];
      this.noResults = false;
      this.currentWordsNumber = 0;
      if (this.enteredWord === "") {
        this.snackbar = true;
        return;
      }
      this.wordsVisible = false;
      this.loader = true;
      this.loadingGoButton = true;
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

      const response = await getRhymes(
        shortLang,
        this.selectedLevel,
        this.enteredWord,
        this.inacuurate
      );
      this.currentReader = ndjsonStream(response.body).getReader();

      let result;
      while (!result || !result.done) {
        result = await this.currentReader.read();
        if (!result.done) {
          this.rhymes.push(result.value);
          this.loader = false;
          this.wordsVisible = true;
          this.currentWordsNumber++;
        } else {
          this.showMore = false;
        }
        if (this.currentWordsNumber >= 70) {
          this.showMore = true;
          break;
        }
      }
      if (this.currentWordsNumber === 0) {
        this.noResults = true;
      } else {
        this.wordsVisible = true;
      }
      this.loadingGoButton = false;
      this.loader = false;
    },
    async showMoreRhymes() {
      this.currentWordsNumber = 0;
      this.rhymes = [];
      this.wordsVisible = false;
      this.loader = true;
      this.loadingShowMoreButton = true;
      let result;
      while (!result || !result.done) {
        result = await this.currentReader.read();
        if (!result.done) {
          this.rhymes.push(result.value);
          this.loader = false;
          this.wordsVisible = true;
          this.currentWordsNumber++;
        } else {
          this.showMore = false;
        }
        if (this.currentWordsNumber >= 70) {
          this.showMore = true;
          break;
        }
      }
      this.wordsVisible = true;
      this.loadingShowMoreButton = false;
      this.loader = false;
    },
  },
};
</script>

<style scoped>
.fade-out-in-enter-active {
  transition: opacity 0.1s;
}
.fade-out-in-leave-active {
  transition: opacity 0.1s;
}
.fade-out-in-enter-active {
  transition-delay: 0.1s;
}

.fade-out-in-enter,
.fade-out-in-leave-to {
  opacity: 0;
}
.list-item {
  display: inline-block;
  margin-right: 10px;
}
.list-enter-active,
.list-leave-active {
  transition: all 1s;
}
.list-enter, .list-leave-to /* .list-leave-active below version 2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}
</style>