import type {UploadFile} from "antd";
import {fetchAPI} from "./index.ts";
import type {ipfsFileType} from "../publicTypes/ipfs.ts";
import type {RcFile} from "antd/es/upload";

export const uploadFile = async (file: RcFile) => {
    const form = new FormData()
    form.append('file', file)
    return fetchAPI.req<ipfsFileType>('/ipfs/upload', {
        method: "POST", body: form
    })
}