export type action = {
    event_name?: string
    input_parameter?: any
    result?: any
    userId?: string
}
export type Log = {
    log_id?: number,
    user_id?: string,
    action: action,
    timestamp: string,
    blockchain_tx_hash: string
    blockchain_block_number: number
    blockchain_operator: string
}