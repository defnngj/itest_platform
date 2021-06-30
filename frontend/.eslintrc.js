module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true
  },
  extends: ['eslint:recommended', 'plugin:vue/essential', 'eslint-config-egg'],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly'
  },
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module'
  },
  plugins: ['vue'],
  rules: {
    quotes: ['error', 'single'],
    semi: 0,
    'comma-dangle': [2, 'never'],
    'array-bracket-spacing': [2, 'never']
  }
}
