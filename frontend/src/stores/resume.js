import { defineStore } from 'pinia'
import axios from 'axios'

export const useResumeStore = defineStore('resume', {
    state: () => ({
        parsedResults: [],
        isParsing: false,
        error: null,
    }),

    actions: {
        async uploadAndParse(file) {
            this.isParsing = true
            this.error = null

            const formData = new FormData()
            formData.append('file', file)

            try {
                const response = await axios.post('http://localhost:8000/api/v1/candidates/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })

                // Response structure from backend: { message, file_name, saved_path, parsed_data }
                const result = response.data.parsed_data
                result.sourceFile = file.name

                this.parsedResults.push(result)

                return true
            } catch (err) {
                console.error('Upload Error for ' + file.name + ':', err)
                this.error = err.response?.data?.detail || err.message || 'Failed to upload and parse resume'
                return false
            } finally {
                this.isParsing = false
            }
        },

        clearData() {
            this.parsedResults = []
            this.error = null
        }
    }
})
