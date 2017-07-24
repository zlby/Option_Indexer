function notifi(title, msg, type, context){
  context.$notify({
    title: title,
    message: msg,
    type: type
  });
}

export {notifi}