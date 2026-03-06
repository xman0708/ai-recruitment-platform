import axios from "axios";
import fs from "fs";
import FormData from "form-data";

fs.writeFileSync("test.txt", "This is a resume of Robin. He knows AI.");
const form = new FormData();
form.append("file", fs.createReadStream("test.txt"));

axios.post("http://localhost:8000/api/v1/candidates/upload", form, {
  headers: { ...form.getHeaders() }
}).then(res => {
  console.log(typeof res.data, res.data);
}).catch(err => {
  console.error("error", err);
});
