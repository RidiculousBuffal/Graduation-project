import type {Point} from "@/components/imageInnot/types"
import type {ipfsFileType} from "@/publicTypes/ipfs.ts";

export type InspectionItemPoint = {
    point: Point
    fileInfo: ipfsFileType
}
export type YoloBox = {
    x1: number,
    x2: number,
    y1: number,
    y2: number,
}
export type YoloDetect = {
    points: YoloBox,
    label: string,
    confidence: number,
}
export type YoloResult = {
    boxes: YoloDetect[]
    resultImage: ipfsFileType,
}
export type InspectionItemResult = {
    resultImage: YoloResult
    isPassed: boolean
    inputImage: ipfsFileType
    progress:"pending"|"detecting"|"done"|"canceled"|"error"
    version: number
}
export type InspectionItem={
    item_id:string,
    item_name: string,
    inspection_id:string,
    item_point:InspectionItemPoint,
    description:string,
    result:Array<InspectionItemResult>,
    model_id:string,
    model_name:string,
    model_description:string,
    created_at:string,
    updated_at:string,
}