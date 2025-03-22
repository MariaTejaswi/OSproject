#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

class DiskScheduling
{
    int head;
    vector<int> requests;

public:
    void getInput()
    {
        int n;
        cout << "Enter number of requests: ";
        cin >> n;

        requests.resize(n);
        cout << "Enter requests: ";
        for (int i = 0; i < n; i++)
        {
            cin >> requests[i];
        }

        cout << "Enter initial head position: ";
        cin >> head;
    }
    void fcfs()
    {
        int seek_time = 0;
        int current_position = head;

        cout << "\nFCFS Order: " << current_position;
        for (int req : requests)
        {
            seek_time += abs(req - current_position);
            current_position = req;
            cout << " -> " << req;
        }
        cout << "\nTotal Seek Time: " << seek_time << "\n";
    }

    void sstf()
    {
        int seek_time = 0;
        int current_position = head;
        vector<int> remaining = requests;

        cout << "\nSSTF Order: " << current_position;
        while (!remaining.empty())
        {
            auto closest = min_element(remaining.begin(), remaining.end(),
                                       [current_position](int a, int b)
                                       {
                                           return abs(a - current_position) < abs(b - current_position);
                                       });
            seek_time += abs(*closest - current_position);
            current_position = *closest;
            cout << " -> " << *closest;
            remaining.erase(closest);
        }
        cout << "\nTotal Seek Time: " << seek_time << "\n";
    }

    void scan()
    {
        int seek_time = 0;
        vector<int> left, right;
        int current_position = head;

        for (int req : requests)
        {
            if (req < head)
                left.push_back(req);
            else
                right.push_back(req);
        }

        sort(left.begin(), left.end(), greater<int>());
        sort(right.begin(), right.end());

        cout << "\nSCAN Order: " << current_position;
        for (int req : right)
        {
            seek_time += abs(req - current_position);
            current_position = req;
            cout << " -> " << req;
        }
        for (int req : left)
        {
            seek_time += abs(req - current_position);
            current_position = req;
            cout << " -> " << req;
        }
        cout << "\nTotal Seek Time: " << seek_time << "\n";
    }

    void cscan()
    {
        int seek_time = 0;
        vector<int> left, right;
        int current_position = head;

        for (int req : requests)
        {
            if (req < head)
                left.push_back(req);
            else
                right.push_back(req);
        }

        sort(left.begin(), left.end());
        sort(right.begin(), right.end());

        cout << "\nC-SCAN Order: " << current_position;
        for (int req : right)
        {
            seek_time += abs(req - current_position);
            current_position = req;
            cout << " -> " << req;
        }

        // Jump to the beginning of the disk
        if (!left.empty())
        {
            seek_time += abs(current_position - left.front());
            current_position = left.front();

            for (int req : left)
            {
                seek_time += abs(req - current_position);
                current_position = req;
                cout << " -> " << req;
            }
        }
        cout << "\nTotal Seek Time: " << seek_time << "\n";
    }
};
int main()
{
    DiskScheduling ds;
    ds.getInput();

    cout << "\nSelect Scheduling Algorithm:\n";
    cout << "1. FCFS\n2. SSTF\n3. SCAN\n4. C-SCAN\n";
    int choice;
    cin >> choice;

    switch (choice)
    {
    case 1:
        ds.fcfs();
        break;
    case 2:
        ds.sstf();
        break;
    case 3:
        ds.scan();
        break;
    case 4:
        ds.cscan();
        break;
    default:
        cout << "Invalid Choice!";
    }

    return 0;
}
