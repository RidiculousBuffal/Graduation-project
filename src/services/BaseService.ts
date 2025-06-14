export class BaseService {
    protected static async processResultAsync(res: any, success: () => Promise<void> = async () => {
    }, fail: () => Promise<void> = async () => {
    }): Promise<boolean> {
        if (res) {
            await success()
            return true
        } else {
            await fail()
            return false
        }
    }

    protected static processResultSync(res: any, success: () => void = () => {
    }, fail: () => void = () => {
    }): boolean {
        if (res) {
            success()
            return true
        } else {
            fail()
            return false
        }
    }

}