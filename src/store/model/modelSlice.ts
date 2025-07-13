import type {EasySlice, MiddlewareTypes} from "@/store/baseType.ts";
import type {model} from "@/store/model/types.ts";
import type {StateCreator} from "zustand/vanilla";
import type {ModelState} from "@/store/model/modelStore.ts";
import {initPagination} from "@/publicTypes/pagination.ts";

export type ModelSlice=EasySlice<'model', model, model>
export const createModelSlice:StateCreator<ModelState,MiddlewareTypes,[],ModelSlice>=(setState, getState, store)=>{
    return {
        models:[],
        modelsPagination:initPagination
        ,
        setModels: (models:model[])=>{
            setState({...getState(),models:models})
        },
        setModelsPagination: (obj)=>{
            setState({...getState(),modelsPagination:obj})
        },
        updateModel: (obj)=>{
            const currentState=getState()
            const newModels=currentState.models.map(x=>{
                if(x.model_id==obj.model_id){
                    return obj
                }else{
                    return x
                }
            })
            setState({...getState(),models:newModels})
        }
    }
}