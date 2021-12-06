<template>
  <v-app id="app">
    <v-app-bar app color="#6e55c6" dark>
      <v-row>
        <v-spacer></v-spacer>
        <v-img
          alt="Vuetify Logo"
          contain
          src="https://www.freepnglogos.com/uploads/music-folder-anything-music-logo-png-2.png"
          transition="scale-transition"
          width="40"
          max-height="80"
          max-width="100"
        />
        <div class="mt-3"><h1 id="top_text">Rhymes Generator!</h1></div>
        <v-spacer></v-spacer>
      </v-row>
    </v-app-bar>

    <v-main>
      <Main />
    </v-main>
  </v-app>
</template>

<script>
import Main from "./components/Main";

export default {
  name: "App",

  components: {
    Main,
  },

  data: () => ({
    //
  }),
};
</script>

<style>
#app {
  background-color: var(--v-background-base);
}
#top_text {
  font-family: "Verdana";
  color: transparent;
  text-shadow: 0 0 2px #ffffff;
}
</style>
