#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

#include <opencv2/opencv.hpp>

struct FramePacket {
    cv::Mat frame;
    std::chrono::steady_clock::time_point captured_at;
};

class FrameQueue {
public:
    void push(const cv::Mat& frame) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (queue_.size() > 10) {
            queue_.pop();
        }
        queue_.push({frame.clone(), std::chrono::steady_clock::now()});
        cv_.notify_one();
    }

    bool pop(FramePacket& packet) {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return !queue_.empty(); });
        if (queue_.empty()) {
            return false;
        }
        packet = queue_.front();
        queue_.pop();
        return true;
    }

private:
    std::queue<FramePacket> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;
};

int main(int argc, char** argv) {
    std::string src = argc > 2 ? argv[2] : "0";
    cv::VideoCapture capture(src);
    if (!capture.isOpened()) {
        std::cerr << "Unable to open source." << std::endl;
        return 1;
    }

    FrameQueue queue;
    std::atomic<int> processed_frames{0};
    std::atomic<double> avg_latency_ms{0.0};

    std::thread capture_thread([&]() {
        cv::Mat frame;
        while (capture.read(frame)) {
            queue.push(frame);
        }
    });

    std::thread processing_thread([&]() {
        FramePacket packet;
        while (queue.pop(packet)) {
            auto begin = std::chrono::steady_clock::now();
            cv::Mat processed = packet.frame.clone();
            if (processed.empty()) {
                continue;
            }
            cv::GaussianBlur(processed, processed, cv::Size(5, 5), 0);
            auto elapsed = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - begin).count();
            avg_latency_ms.store(avg_latency_ms.load() + elapsed);
            processed_frames.fetch_add(1);
        }
    });

    capture_thread.join();
    processing_thread.join();

    std::cout << "Processed frames: " << processed_frames.load() << std::endl;
    std::cout << "Average latency ms: " << (processed_frames.load() ? avg_latency_ms.load() / processed_frames.load() : 0.0) << std::endl;
    return 0;
}
