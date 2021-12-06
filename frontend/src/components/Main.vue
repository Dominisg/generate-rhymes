<template>
  <v-contaier fill-height fluid>
    <v-row align="center" justify="center" class="mt-10">
      <v-col cols="6">
        <v-row>
          <v-card width="100%">
            <v-card-text>
              <v-row>
                <v-select
                  :items="languages"
                  label="Language"
                  outlined
                  class="ma-5"
                ></v-select>
                <v-text-field
                  label="Word"
                  :rules="rules"
                  hide-details="auto"
                  outlined
                  class="ma-5"
                ></v-text-field>
              </v-row>
              <v-row align="center" justify="center" class="mb-3">
                <v-btn color="green"> Go!</v-btn>
              </v-row>
            </v-card-text>
          </v-card>
        </v-row>
        <v-row class="mt-10">
          <v-card width="100%">
            <v-card-text>
              <v-row> </v-row>
            </v-card-text>
          </v-card>
        </v-row>
      </v-col>
    </v-row>
    <v-row> </v-row>
  </v-contaier>
</template>

<script>
export default {
  name: "Main",

  components: {},

  data: () => ({
    languages: ["English", "Polish"],
  }),
};
</script>

<style>
</style>