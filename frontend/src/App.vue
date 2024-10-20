<template>
  <div class="container">
    <input v-model="inputValue" />
    <button @click="sendRequest">提交</button>
    <button @click="pasteFromClipboard">粘贴</button>
      <button @click="clearInput">清空</button>
    <div class="content">{{ content }}</div>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
export default {
  setup() {
    const inputValue = ref('');
    const content = ref('');
    const backend = '';
    const sendRequest = () => {
      axios.post(backend+'/hello', { input: inputValue.value })
        .then(response => {
          content.value = response.data.result;
        })
        .catch(error => {
          content.value = error.message;
        });
    };
    const pasteFromClipboard = async () => {
      try {
        const text = await navigator.clipboard.readText();
        inputValue.value = text;
      } catch (error) {
        content.value = '粘贴失败: ' + error.message;
      }
    };

    const clearInput = () => {
      inputValue.value = '';
    };

    return {
      inputValue,
      content,
      sendRequest,
      clearInput,
      pasteFromClipboard,
    };
  }
};
</script>

<style scoped>
.container {
  background-color: white;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

input {
  display: block;
  margin-bottom: 20px;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  color: white;
  border: none;
  cursor: pointer;
}

.content {
  margin-top: 20px;
  color: #333;
}
</style>

